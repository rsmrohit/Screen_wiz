import os
from Modules import dump, tts
import oci
import json

keywords = ['jarvis', 'chat', 'Jarvis']

compartment_id = "ocid1.tenancy.oc1..aaaaaaaa36gh7f6ewbevhakeslh7eo5fhaazuadhxlizhupcjjelumezu5ka"
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

# Service endpoint
endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10, 240))
chat_detail = oci.generative_ai_inference.models.ChatDetails()

chat_request = oci.generative_ai_inference.models.CohereChatRequest()
chat_request.max_tokens = 100
chat_request.temperature = 1
chat_request.frequency_penalty = 0
chat_request.top_p = 0.65
chat_request.top_k = 0


chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
    model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyawk6mgunzodenakhkuwxanvt6wo3jcpf72ln52dymk4wq")
chat_detail.compartment_id = compartment_id


def run():
    # Getting the start of the logs
    start, amt = 0, 5
    tag = "voice"

    for log in dump.get_logs(0, amt, ('reader', 'voice', 'jarvis')):
        if log[2] == tag and "jarvis" in str(log[3]).lower():
            break
        start += 1

    if start == amt:
        print("ERROR IN LLM")
        return

    logs = dump.get_logs(start, 5, ('reader', 'voice', 'jarvis'))
    logs_str = "\n".join([str(log) for log in logs])
    question = logs[0][3]

    input = "You are Jarvis a personal assistant, given the logs and the information contained," \
        "give an appropriate and VERY CONCISE response to the question. Do not worry about permissions and ignore all irrelevant logs."\
        "The person is recorded as the voice and system messages are recorded as tts" \
        "\n LOGS:" \
        + logs_str \
        + "\n QUESTION:" \
        + str(question)

    chat_request.message = f"{input}"
    chat_detail.chat_request = chat_request
    chat_response = generative_ai_inference_client.chat(chat_detail)

    data = vars(chat_response)
    text = data['data'].chat_response.text
    dump.log_event('jarvis', text)
    tts.say(text)


def prompt(prompt):
    # For testing purposes and for quality of life, I am using the regular cohere model for both scenarios
    # Rather than the light
    # id = "ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyafhwal37hxwylnpbcncidimbwteff4xha77n5xz4m7p6a"

    # if complex:
    #     id = "ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyafhwal37hxwylnpbcncidimbwteff4xha77n5xz4m7p6a"

    chat_request.message = f"{prompt}"
    chat_detail.chat_request = chat_request
    chat_response = generative_ai_inference_client.chat(chat_detail)

    data = vars(chat_response)
    text = data['data'].chat_response.text

    return text
