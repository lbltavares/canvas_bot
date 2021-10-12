from typing import Any, Callable
import config
import api
import util
import cache

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from logger import LoggerFactory

# # Enable logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )

# logger = logging.getLogger(__name__)

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Telegram.LOG_LEVEL)

# Create the Updater and pass it your bot's token.
_updater = Updater(
    token=config.Telegram.TELEGRAM_TOKEN, use_context=True)


def get_bot():
    return _updater.bot


def send_message(msg):
    bot = get_bot()
    chat_id = int(config.Telegram.TELEGRAM_CHAT_ID)
    bot.send_message(chat_id=chat_id, text=msg)


def authorized_only(command_handler: Callable[..., None]) -> Callable[..., Any]:
    """
    Decorator to check if the message comes from the correct chat_id
    :param command_handler: Telegram CommandHandler
    :return: decorated function
    """

    def wrapper(*args, **kwargs):
        """ Decorator logic """
        update = kwargs.get('update') or args[0]

        # Log message
        # Get username
        username = update.effective_user.username
        _log.info(
            f"{username}::{update.effective_chat.id} - {update.effective_message.text}")

        # Reject unauthorized messages
        if update.callback_query:
            cchat_id = int(update.callback_query.message.chat.id)
        else:
            cchat_id = int(update.message.chat_id)

        chat_id = int(config.Telegram.TELEGRAM_CHAT_ID)
        if cchat_id != chat_id:
            _log.warning(
                'Rejected unauthorized message from: %s',
                update.message.chat_id
            )
            return wrapper

        _log.debug(
            'Executing handler: %s for chat_id: %s',
            command_handler.__name__,
            chat_id
        )
        try:
            return command_handler(*args, **kwargs)
        except BaseException:
            _log.exception('Exception occurred within Telegram module')

    return wrapper


@authorized_only
def calendario(update: Update, context: CallbackContext) -> None:
    pass


@authorized_only
def proximas(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    parts = text.split()
    limit = 3
    if len(parts) > 1:
        try:
            limit = max(min(int(parts[1]), 10), 1)
        except Exception:
            pass

    prox = api.proximas(limit)
    prox = [util.format_tarefa(p, c.name) for c, p in prox]
    prox = ('\n' + '-'*30 + '\n').join(prox)
    update.message.reply_html(f"<pre>\n{prox}\n</pre>")


@authorized_only
def get_all(update: Update, context: CallbackContext) -> None:
    prox = api.proximas()
    prox = [util.format_tarefa(p, c.name) for c, p in prox]
    prox = ('\n' + '-'*30 + '\n').join(prox)
    update.message.reply_html(f"<pre>\n{prox}\n</pre>")


@authorized_only
def courses(update: Update, context: CallbackContext) -> None:
    courses = api.courses()
    msg = "<pre>\n"
    msg += "ID     | Course \n"
    maxlength = 22
    msg += '-' * (maxlength+9) + '\n'
    for name, id in courses:
        name = (name[:maxlength] + '...') if len(name) > maxlength else name
        name = name.strip()
        msg += f"%-7s| %-{maxlength}s\n" % (str(id), name)
    msg += "</pre>"
    update.message.reply_html(msg)


@authorized_only
def merge(update: Update, context: CallbackContext) -> None:
    # Get user text
    text = update.message.text
    if len(text.split()) < 2:
        update.message.reply_text("Merge deve ser chamado com o ID do curso")
        return

    course_id = text.split()[1]
    try:
        course_id = int(course_id.strip())
    except Exception:
        update.message.reply_text("O course_id precisa ser um numero")
        return

    result = api.merge(
        course_id,
        start_download_cb=lambda c: update.message.reply_text(
            f'Baixando arquivos de: {c.name.split("-")[0].title()}'),
        end_download_cb=lambda c, f: update.message.reply_text(
            f'Download concluido. Total: {len(f)} arquivos.'),
        start_merge_cb=lambda c: update.message.reply_text(
            f'Iniciando o merge...'),
        end_merge_cb=lambda c: update.message.reply_text(
            f'Merge finalizado com sucesso.'))

    try:
        fpath = result['merge_path']
        fname = result['merge_filename']
        files_merged = result['files_merged']
        files_merged = [f[:45] + '...' + f[-5:]
                        if len(f) > 50
                        else f
                        for f in files_merged]
        files_merged = '\n'.join(files_merged)
        msg = "<pre>Arquivos do merge:\n" + files_merged + "</pre>"
        update.message.reply_html(msg)
        context.bot.send_document(
            chat_id=update.message.chat_id,
            document=open(fpath, 'rb'),
            filename=fname
        )
    except Exception as e:
        update.message.reply_text(f"Erro: {e}")


@authorized_only
def pontos(update: Update, context: CallbackContext) -> None:
    pass


@authorized_only
def update(update: Update, context: CallbackContext) -> None:
    if not config.Cache.ENABLE:
        update.message.reply_text('Cache refresh desabilitado')
        return
    update.message.reply_text("Atualizando cache...")
    cache.atualizar()
    last = cache.last_update_formatted()
    update.message.reply_text(f"Cache atualizado em {last}")


@authorized_only
def notificar(update: Update, context: CallbackContext) -> None:
    config.Notif.ENABLE = not config.Notif.ENABLE
    enabled = config.Notif.ENABLE
    symbol = '\U0001F7E2' if enabled else '\U0001F534'
    update.message.reply_text(
        f"{symbol} Notificacoes {'ativadas' if enabled else 'desativadas'}\n" +
        f"Notificacoes: {enabled}\n" +
        f"Intervalo: {config.Notif.CHECK_INTERVAL_M}m\n"
    )


@authorized_only
def automerge(update: Update, context: CallbackContext) -> None:
    config.Merge.ENABLE = not config.Merge.ENABLE
    enabled = config.Merge.ENABLE
    symbol = '\U0001F7E2' if enabled else '\U0001F534'
    update.message.reply_text(
        f"{symbol} Automerge {'ativado' if enabled else 'desativado'}\n"
        f"Automerge: {enabled}\n" +
        f"Intervalo: {config.Merge.CHECK_INTERVAL_M}m\n"
    )


def init() -> None:
    """Start the bot."""

    # Get the dispatcher to register handlers
    dispatcher = _updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("calendario", calendario))
    dispatcher.add_handler(CommandHandler("proximas", proximas))
    dispatcher.add_handler(CommandHandler("all", get_all))
    dispatcher.add_handler(CommandHandler("courses", courses))
    dispatcher.add_handler(CommandHandler("merge", merge))
    dispatcher.add_handler(CommandHandler("pontos", pontos))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("notificar", notificar))
    dispatcher.add_handler(CommandHandler("automerge", automerge))

    # Start the Bot
    _updater.start_polling(
        bootstrap_retries=-1,
        timeout=30,
        read_latency=60,
        drop_pending_updates=True,
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    _updater.idle()
