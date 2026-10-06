<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/hero-dark.svg" />
  <img src="./assets/hero-light.svg" alt="Taiheng Pan. I help language models learn better, and help agents remember what matters." width="100%" />
</picture>

<p align="center">
  <a href="https://arxiv.org/abs/2610.02911"><img src="https://img.shields.io/badge/arXiv-2610.02911-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white" alt="arXiv 2610.02911" /></a>
  <a href="https://huggingface.co/Purdy0228"><img src="https://img.shields.io/badge/Hugging_Face-Purdy0228-f5b301?style=for-the-badge&logo=huggingface&logoColor=white" alt="Hugging Face" /></a>
  <a href="https://github.com/NoetixAI"><img src="https://img.shields.io/badge/NoetixAI-organization-1f2328?style=for-the-badge&logo=github&logoColor=white" alt="NoetixAI" /></a>
</p>

<h3 align="center">Hi, I'm Taiheng. I make the best.</h3>

I love the moment a result has to stand up for itself. Reinforcement learning for LLMs, memory for long-running agents, evaluation that holds up under a second look: that is where I spend my days, and everything below ships with code you can run today.

## <img src="./assets/mark-probe.svg" width="26" height="26" alt="" /> Probe the Harness

<a href="https://github.com/pth2002/probe-the-harness"><img src="https://img.shields.io/badge/code-probe--the--harness-0d1117?style=flat-square&logo=github" alt="Code" /></a>
<a href="https://arxiv.org/abs/2610.02911"><img src="https://img.shields.io/badge/paper-arXiv_2610.02911-b31b1b?style=flat-square" alt="Paper" /></a>
<a href="https://pypi.org/project/probe-the-harness/"><img src="https://img.shields.io/pypi/v/probe-the-harness?style=flat-square&label=pip%20install%20probe-the-harness" alt="PyPI" /></a>

**My new RL method won every single run. So I went bug hunting.**

Before claiming the win, I audited the training harness and caught four bugs propping it up, each one hiding behind a log that looked perfectly healthy. With all four fixed, the clean sweep became an honest tie. I packaged that hunt into PTH: point it at your verl logs and it runs the same four checks in one command, so the next surprising win in your lab gets the scrutiny it deserves.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/bugs-dark.svg" />
  <img src="./assets/bugs-light.svg" alt="The four bugs: the Idle Clip, the Lost Seed, the Stuck Batch and the Rogue Normaliser." width="100%" />
</picture>

Here is the Idle Clip caught in a real run. The clip fraction read a calm 0.000 on every update, while the sampler drifted ten thousand times further from the learner.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pth2002/probe-the-harness/main/assets/signal-dark.svg" />
  <img src="https://raw.githubusercontent.com/pth2002/probe-the-harness/main/assets/signal-light.svg" alt="Sampler to learner KL grows by four orders of magnitude while the PPO clip fraction stays at zero." width="100%" />
</picture>

## <img src="./assets/mark-memory.svg" width="26" height="26" alt="" /> ConvMemory

<a href="https://github.com/pth2002/ConvMemory"><img src="https://img.shields.io/badge/code-ConvMemory-0d1117?style=flat-square&logo=github" alt="Code" /></a>
<a href="https://huggingface.co/Purdy0228/ConvMemory-LoCoMo-MPNet"><img src="https://img.shields.io/badge/checkpoint-Hugging_Face-f5b301?style=flat-square&logo=huggingface&logoColor=white" alt="Checkpoint" /></a>
<a href="https://pypi.org/project/convmemory/"><img src="https://img.shields.io/pypi/v/convmemory?style=flat-square&label=pip%20install%20convmemory" alt="PyPI" /></a>

**Cross-encoder quality for agent memory, at a fraction of the wait.**

ConvMemory is a 14 MB reranker that slots in between your vector search and your agent. On LoCoMo it beats both BGE cross-encoders on Recall@10 and MRR in 28.6 ms per query, and lands within 2% of mxbai-rerank-large's MRR while running 68 times faster. Plug it into mem0, LangChain or LlamaIndex in about ten lines. And if you are curious how I test my own ideas, the repo includes [the five-seed study](https://github.com/pth2002/ConvMemory/blob/main/docs/posts/i-was-wrong-about-temporal-memory.md) that overturned my first explanation of why it works.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pth2002/ConvMemory/main/docs/assets/pareto-dark.png" />
  <img src="https://raw.githubusercontent.com/pth2002/ConvMemory/main/docs/assets/pareto-light.png" alt="Retrieval quality against reranking latency on LoCoMo." width="100%" />
</picture>

## <img src="./assets/mark-built.svg" width="26" height="26" alt="" /> More I've built

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/cards-dark.svg" />
  <img src="./assets/cards-light.svg" alt="FinPilot: 74 percent preference win rate. Bilingual contract RAG: Chinese Recall@5 up 93 percent." width="100%" />
</picture>

**[FinPilot](https://github.com/pth2002/FinPilot): a 3B model that talks markets.** I trained Qwen2.5-3B with SFT and then DPO into an assistant for A-share investing, and a GPT-4o judge preferred its answers 74% of the time.

**[BiLegalContract-RAG-Tool](https://github.com/pth2002/BiLegalContract-RAG-Tool): long contracts, two languages, one assistant.** Hybrid retrieval, cross-encoder reranking and a critic-and-reflection loop read contracts in Chinese, English or both. Clause-aware chunking alone lifted Chinese Recall@5 by 93%.

## <img src="./assets/mark-bring.svg" width="26" height="26" alt="" /> What I bring

I treat evaluation as part of the product. Every comparison I run starts by checking the baseline, every claim ships with the code to reproduce it, and when the evidence changes the story, I change the story and say so out loud. That makes my wins a little rarer and a lot harder to argue with.

## <img src="./assets/mark-stack.svg" width="26" height="26" alt="" /> Toolbox

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/toolbox-dark.svg" />
  <img src="./assets/toolbox-light.svg" alt="My toolbox as a transit map: training, memory, product and research lines, all starting from Python." width="100%" />
</picture>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/stack-icons-dark.svg" />
    <img src="./assets/stack-icons-light.svg" alt="Python, PyTorch, Hugging Face, FastAPI, TypeScript, React, Vite, PostgreSQL, Docker, Linux, Git, GitHub, GitHub Actions, LaTeX and R" width="100%" />
  </picture>
</p>

## <img src="./assets/mark-year.svg" width="26" height="26" alt="" /> A year of building

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pth2002/pth2002/output/contributions-dark.svg" />
  <img src="https://raw.githubusercontent.com/pth2002/pth2002/output/contributions-light.svg" alt="A year of contributions, with a snake eating its way through every active day." width="100%" />
</picture>

<p align="center"><sub>Redrawn every day by GitHub Actions from my contribution calendar.</sub></p>
