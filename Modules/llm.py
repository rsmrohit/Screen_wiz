import os
from Modules import dump, tts
import oci
import json

keywords = ['jarvis', 'chat', 'Jarvis']

compartment_id = "ocid1.tenancy.oc1..aaaaaaaa36gh7f6ewbevhakeslh7eo5fhaazuadhxlizhupcjjelumezu5ka"
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10, 240))
generate_text_detail = oci.generative_ai_inference.models.GenerateTextDetails()
llm_inference_request = oci.generative_ai_inference.models.CohereLlmInferenceRequest()
llm_inference_request.max_tokens = 200
llm_inference_request.temperature = 3.7
llm_inference_request.frequency_penalty = 0
llm_inference_request.top_p = 0.75
generate_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
    model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyafhwal37hxwylnpbcncidimbwteff4xha77n5xz4m7p6a")


def run():

    # Getting the start of the logs
    start, amt = 0, 5
    tag = "voice"

    for log in dump.get_logs(0, amt):
        if log[2] == tag and "jarvis" in str(log[3]).lower():
            break
        start += 1

    if start == amt:
        print("ERROR IN LLM")
        return

    logs = dump.get_logs(start, 5)
    logs_str = "\n".join(str(logs[1:][1:]))
    question = logs[0][3]

    llm_inference_request.prompt = "You are Jarvis a personal assistant, given the logs and the information contained," \
        "give an appropriate and concise response to the question. Do not worry about permissions and ignore all irrelevant logs."\
        "The person is recorded as the voice and system messages are recorded as tts" \
        "\n LOGS:" \
        + logs_str \
        + "\n QUESTION:" \
        + str(question)

    generate_text_detail.inference_request = llm_inference_request
    generate_text_detail.compartment_id = compartment_id
    generate_text_response = generative_ai_inference_client.generate_text(
        generate_text_detail)
    # Print result
    # print("**************************Generate Texts Result**************************")
    data = generate_text_response.data
    text = data.inference_response.generated_texts[0].text
    dump.log_event('llm', text)
    tts.say(text)
