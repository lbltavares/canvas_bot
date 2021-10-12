from typing import Any, Callable
import config
import api
import util
import cache

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from logger import LoggerFactory

# # Enable logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )

# logger = logging.getLogger(__name__)

_log = LoggerFactory.get_default_logger(__name__, filename=config.get(
    'log_filename', 'app.log') if config.get('unique_log_file') else None)
_log.setLevel(config.get('telegram_bot_log_level', 'INFO'))


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
        _log.info(f"{update.effective_chat.id} - {update.effective_message.text}")

        # Reject unauthorized messages
        if update.callback_query:
            cchat_id = int(update.callback_query.message.chat.id)
        else:
            cchat_id = int(update.message.chat_id)

        chat_id = int(config.get('telegram_chat_id'))
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


def calendario(update: Update, context: CallbackContext) -> None:
    pass


def proximas(update: Update, context: CallbackContext) -> None:
    prox = api.proximas(3)
    prox = [util.format_tarefa(p, c) for c, p in prox]
    prox = ('\n' + '-'*30 + '\n').join(prox)
    update.message.reply_html(f"<pre>\n{prox}\n</pre>")


@authorized_only
def get_all(update: Update, context: CallbackContext) -> None:
    prox = api.proximas()
    prox = [util.format_tarefa(p, c) for c, p in prox]
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
        msg = "<pre>Arquivos que foram juntados:\n" + files_merged + "</pre>"
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
    if not config.get('enable_cache_refresh'):
        update.message.reply_text('Cache refresh desabilitado')
        return
    update.message.reply_text("Atualizando cache...")
    cache.update()
    last = cache.last_update_formatted()
    update.message.reply_text(f"Cache atualizado em {last}")


@authorized_only
def notificar(update: Update, context: CallbackContext) -> None:
    pass


@authorized_only
def automerge(update: Update, context: CallbackContext) -> None:
    pass


@authorized_only
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


@authorized_only
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def init() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=config.get('telegram_token'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    filter = Filters.chat(config.get('telegram_chat_id'))
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
    updater.start_polling(
        bootstrap_retries=-1,
        timeout=30,
        read_latency=60,
        drop_pending_updates=True,
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
