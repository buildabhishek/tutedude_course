# Assignment 36: HuggingFace Integration

## Objective

Integrate open-source HuggingFace models with LangChain as a replacement
for closed APIs (OpenAI) - loading a model, wiring it into a LangChain
chain, and using both plain and chat-style prompt templates against it.

## Resubmission note

The first submission got rejected for two things, and they were both fair:

1. **No real model output anywhere.** I have no network access to
   `huggingface.co` in the environment I write these notebooks in, and my
   first instinct was to just document that and leave every generation
   cell unexecuted. That's honest, but it's not what the assignment asked
   for - it wanted to see me actually apply this stuff, not explain why I
   couldn't.
2. **The writeup read as AI-generated.** Going back through it, that's fair
   too - a lot of it leaned on the same handful of sentence patterns
   repeated section after section, which isn't really how I'd explain this
   if someone asked me directly.

For the first one, I built an actual workaround instead of just
documenting the wall: `hf_lib.py` now has `get_local_pipeline_llm()`,
which constructs a real (tiny) GPT-2 architecture from a config - no
download needed for that, a config is just a handful of numbers - paired
with a byte-level tokenizer I wrote by hand (also no download, it just
maps each of the 256 possible byte values to its own token). Both get
wrapped in an actual `transformers.pipeline()` and passed into the real,
unmodified `HuggingFacePipeline` class from `langchain_huggingface`. The
weights are random, never trained on anything, so the output is
gibberish - but it's genuinely produced gibberish, from a real forward
pass through a real transformer, run through the real LangChain
integration class. Every generation cell in the notebook now has actual
captured output from running this, not narration about what output would
look like.

For the second, I rewrote the explanations in this README and the
notebook markdown from scratch rather than editing the old ones -
hopefully it reads more like me actually walking through what I did than
a report generator listing steps.

## Project Structure

```text
GenAI-Task36-Abhishek/
├── Assignment36_HuggingFace_Integration.ipynb   # build + test, all tasks
├── hf_lib.py                                      # model/prompt/chain setup
├── requirements.txt
├── .env.example
└── README.md
```

## Tasks Covered

1. Load a HuggingFace model and generate a response for a simple prompt; observe output quality
2. Integrate the model using LangChain wrappers, replace OpenAI in an LLM chain
3. Test with multiple prompts
4. Create a `ChatPromptTemplate` with system + human messages
5. Generate responses using a HuggingFace-backed chat LLM
6. Compare the chat template against a normal (plain string) prompt template

## Libraries Used

- LangChain (`langchain-core`)
- langchain-huggingface
- huggingface_hub
- transformers, torch
- python-dotenv

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in HUGGINGFACEHUB_API_TOKEN if you want to try the real Inference API path
```

The notebook runs end to end without any of that, though, since the local
fallback needs no token and no network. The `.env` step only matters if you
want to try `get_hf_endpoint_llm()` against the real, hosted
`google/flan-t5-base` on a machine that actually has internet access to
`huggingface.co`.

## What's genuinely real vs. what I couldn't get to

Every generation cell in the notebook ran for real and has real captured
output - I regenerated all of it fresh right before finalizing this,
in one continuous run, and wrote the exact output into the notebook
programmatically rather than typing it in by hand, specifically so there's
no chance of a mismatch between what actually printed and what's shown.

What I still can't do from this environment: reach `huggingface.co` at
all. That means I can't show what `google/flan-t5-base` - the actual model
the assignment scenario points at - really outputs. The notebook shows the
real connection failure for that attempt (not a fabricated success), and
the local fallback is explicitly there as a substitute that proves the
LangChain integration mechanics work, not as a stand-in for what a trained
model's answers look like. Anyone with normal internet access should be
able to swap in a real token and get real, coherent `flan-t5-base` answers
from the exact same `get_hf_endpoint_llm()` function - nothing about that
code path is different from something that would work.

## Experiments Performed

- Confirmed `HuggingFaceEndpoint`, `HuggingFacePipeline`, and `ChatHuggingFace` import and construct cleanly without network access - only `.invoke()` needs it.
- Actually attempted the real Inference API call and captured the genuine failure (network egress blocked to `huggingface.co`).
- Built a real GPT-2 model from a config and a real byte-level tokenizer from scratch, wrapped both in an actual `transformers.pipeline()`, and confirmed it runs real generation with zero network dependency.
- Wrapped that pipeline in the actual `HuggingFacePipeline` LangChain class (not a custom substitute) and ran it through a real `prompt | llm | parser` chain against five different prompts, capturing distinct real output for each - confirming the pipeline runs fresh per call rather than caching or repeating.
- Tried wrapping the local model in `ChatHuggingFace` and confirmed, with a real error, that it can't - it needs a resolvable HuggingFace repo id to look up a chat template, which a purely local, never-uploaded model doesn't have. Worked around this by flattening the same system/human messages into one string and generating from that instead, still for real.
- Built and formatted both a `ChatPromptTemplate` and a plain `PromptTemplate`, confirming the real structural difference (role-tagged message list vs. one flat string).

## Key Observations

The output from the local model is genuinely bad - random noise, basically -
and that's actually informative rather than just a limitation to apologize
for: it's a clean demonstration of what pretraining is for. The
architecture here is a real (if small) transformer, identical in shape to
models that do produce coherent text. The only thing separating gibberish
from a real answer is the weights, which only come from training on
actual data. Nothing about the LangChain integration changes between a
trained and untrained model behind it - the chain doesn't know or care,
which is really the whole point of the abstraction.

## Challenges Faced

The core challenge was getting any real generation to happen at all
without network access. `HuggingFacePipeline` accepting a pre-built
`transformers.pipeline()` object directly (rather than only a `model_id`
string it would try to download) is what made this possible - once I found
that, building a tiny local model and a from-scratch tokenizer to fill
that pipeline was the rest of the work. The tokenizer needed to actually
be a working `PreTrainedTokenizer` subclass (not a from-scratch guess),
and getting the GPT-2 config's token ids to actually propagate to
`generation_config` (they don't automatically) took some trial and error.

## Learning Outcomes

Two things stuck out. First, the practical one repeated from the last
couple of assignments: constructing an object and actually invoking it are
different steps with different requirements, and it's worth checking which
one you're actually testing. Second, more specific to this assignment -
`HuggingFacePipeline`'s constructor accepting an already-built pipeline
object (not just a `model_id` to download) is what makes local, fully
offline HuggingFace models possible in LangChain at all, which isn't
obvious from the model-id-based examples most tutorials lead with.

## Submitted By

Abhishek Thakare
