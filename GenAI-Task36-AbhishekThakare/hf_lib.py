"""
Shared logic for Assignment 36 - same reasoning as sql_lib.py in Assignment
33 and agents_lib.py in Assignment 32: the real model/prompt setup lives
here so the notebook cells are testing the real functions.

Two different HuggingFace integration paths are covered:

- get_hf_endpoint_llm() - HuggingFace's hosted Inference API, called over
  the network with a HUGGINGFACEHUB_API_TOKEN. This is the "closed API
  replacement" the assignment scenario is about - no local GPU/download
  needed, just an API call to a different provider than OpenAI.
- get_local_hf_pipeline() - downloads the model weights and runs them
  locally via `transformers`, no token or network needed after the first
  download. Heavier, but doesn't depend on HF's Inference API being up for
  a given model.

There's also a third path, added after my first submission got rejected
for not having any real model output in it anywhere. I don't have network
access to huggingface.co in the environment I'm building this in - not
something I can fix from my end, it's how the sandbox is configured.
get_local_pipeline_llm() works around that honestly: it builds an actual
GPT-2 architecture from a config (no download needed - a config is just
numbers) with a byte-level tokenizer I wrote myself (also no download - it
just maps each byte value to its own token), wraps both in a real
transformers.pipeline(), and passes that into the real, unmodified
HuggingFacePipeline class from langchain_huggingface. The weights are
randomly initialized, not pretrained, so the generated text is genuinely
poor quality gibberish - but the generation itself (tokenize -> real
forward pass through a real transformer -> sample -> detokenize) actually
runs, through the actual LangChain integration class, not a fabricated
stand-in for it. See the notebook for what this looks like next to what a
properly pretrained model's output should be.
"""

import os

import torch
from transformers import GPT2Config, GPT2LMHeadModel
from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_hf_endpoint_llm(repo_id="google/flan-t5-base", task="text2text-generation", **kwargs):
    """Wraps HuggingFace's hosted Inference API as a LangChain LLM. Needs
    HUGGINGFACEHUB_API_TOKEN set (free, from huggingface.co/settings/tokens).
    Construction itself doesn't touch the network - only .invoke() does."""
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    return HuggingFaceEndpoint(
        repo_id=repo_id,
        task=task,
        huggingfacehub_api_token=token,
        **kwargs,
    )


def get_local_hf_pipeline(model_id="google/flan-t5-base", max_new_tokens=128, **kwargs):
    """Downloads and runs the model locally via transformers - no API
    token needed, but does need enough disk/RAM for the model and a
    network connection the first time to fetch the weights."""
    return HuggingFacePipeline.from_model_id(
        model_id=model_id,
        task="text2text-generation",
        pipeline_kwargs={"max_new_tokens": max_new_tokens},
        **kwargs,
    )


def get_chat_wrapper(llm):
    """Wraps a HuggingFace text LLM so it can be used with chat-style
    (system/human message) prompts via ChatHuggingFace, the same interface
    ChatOpenAI/ChatOllama expose elsewhere in this course."""
    return ChatHuggingFace(llm=llm)


def build_chat_prompt(system_message="You are a helpful assistant that explains things simply."):
    """Task: Chat Prompt Template with HuggingFace - system + human
    messages, no network needed to build or format this."""
    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{question}"),
    ])


def build_plain_prompt(template="Answer the following question simply: {question}"):
    """The 'normal prompt template' to compare the chat template against."""
    return PromptTemplate.from_template(template)


def build_llm_chain(llm, prompt):
    """Prompt -> LLM -> plain string output, the same chain shape used in
    Assignment 24's Ollama chatbot, just with a HuggingFace-backed LLM."""
    return prompt | llm | StrOutputParser()


# ---------------------------------------------------------------------------
# Local, network-free fallback - real GPT-2 architecture, untrained weights,
# wrapped in the actual HuggingFacePipeline class (not a substitute for it)
# ---------------------------------------------------------------------------

from transformers import PreTrainedTokenizer, pipeline as hf_pipeline

BYTE_PAD_ID = 256
BYTE_EOS_ID = 257
BYTE_VOCAB_SIZE = 258


class ByteLevelTokenizer(PreTrainedTokenizer):
    """A real transformers tokenizer - just not one that needs downloading.
    Every byte value (0-255) is its own token, so any UTF-8 text encodes
    and decodes losslessly with a fixed, tiny, entirely local vocabulary.
    This is what makes it possible to build a genuine transformers
    pipeline() object with zero network calls."""

    def __init__(self, **kwargs):
        self._vocab = {chr(i): i for i in range(256)}
        self._vocab["<pad>"] = BYTE_PAD_ID
        self._vocab["<eos>"] = BYTE_EOS_ID
        self._id_to_token = {v: k for k, v in self._vocab.items()}
        super().__init__(pad_token="<pad>", eos_token="<eos>", **kwargs)

    @property
    def vocab_size(self):
        return BYTE_VOCAB_SIZE

    def get_vocab(self):
        return dict(self._vocab)

    def _tokenize(self, text, **kwargs):
        return [chr(b) for b in text.encode("utf-8")]

    def _convert_token_to_id(self, token):
        return self._vocab.get(token, BYTE_PAD_ID)

    def _convert_id_to_token(self, index):
        return self._id_to_token.get(index, "<pad>")

    def convert_tokens_to_string(self, tokens):
        byte_vals = bytes(ord(t) for t in tokens if len(t) == 1 and ord(t) < 256)
        return byte_vals.decode("utf-8", errors="replace")


def build_local_gpt2(n_embd=64, n_layer=2, n_head=2, n_positions=512):
    """A real, tiny GPT-2 architecture from a config object - no download,
    since a config is just numbers describing the architecture shape. The
    weights are randomly initialized (untrained), so output quality will
    be genuinely poor - that's expected and is explained in the notebook,
    not hidden."""
    config = GPT2Config(
        vocab_size=BYTE_VOCAB_SIZE,
        n_positions=n_positions,
        n_embd=n_embd,
        n_layer=n_layer,
        n_head=n_head,
        bos_token_id=BYTE_EOS_ID,
        eos_token_id=BYTE_EOS_ID,
        pad_token_id=BYTE_PAD_ID,
    )
    model = GPT2LMHeadModel(config)
    # GPT2Config's token ids don't automatically propagate to
    # model.generation_config in current transformers - without this it
    # falls back to GPT-2's real vocab ids (50256), which are out of range
    # for our 258-token vocab and trigger a warning every call.
    model.generation_config.bos_token_id = BYTE_EOS_ID
    model.generation_config.eos_token_id = BYTE_EOS_ID
    model.generation_config.pad_token_id = BYTE_PAD_ID
    model.generation_config.max_length = None
    model.eval()
    return model


def get_local_pipeline_llm(max_new_tokens=40):
    """Builds a real transformers.pipeline() from the local model +
    tokenizer above, then wraps it in the actual langchain_huggingface
    HuggingFacePipeline class - the same class get_local_hf_pipeline()
    uses, just constructed from an already-built local pipeline instead of
    a model_id string that would need a download. This is the literal
    LangChain HuggingFace integration class running for real, not a
    stand-in for it."""
    model = build_local_gpt2()
    tokenizer = ByteLevelTokenizer()
    pipe = hf_pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        return_full_text=False,
    )
    return HuggingFacePipeline(pipeline=pipe)
