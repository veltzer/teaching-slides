---
tags:
- concepts:ai
- concepts:llm
- concepts:agents
level: beginner
category: ai
audience:
- audiences:managers
- audiences:developers

---

# AI Everywhere
## One Technology, Every Field of Human Endeavour
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/ai_everywhere/title.svg)

---

## What This Talk Covers

1. The vocabulary: a dozen AI concepts, one line each
1. How the pieces fit together into a working assistant
1. A grand tour: AI in medicine, finance, law, science, farming...
1. ...and in art, music, film, sports, and archaeology
1. The common pattern behind every one of these stories
1. Software is just *one* stop on this tour — not the destination

---

## The Vocabulary: Talking to a Model

- **Model (LLM)** — a program trained on vast amounts of text that understands and generates language
- **Token** — the small chunk of text a model reads and writes; roughly three quarters of a word
- **Prompt** — the request you write; writing good ones is a craft of its own
- **Context window** — the model's short-term memory: everything it can see at once
- **Roles** — the labels that structure a conversation: system instructions, user questions, assistant answers
- **Multimodal** — a model that also sees images and hears audio, not just text
- **Hallucination** — a confident, fluent answer that is simply made up

---

## The Vocabulary: From Chatbot to Agent

- **Tool** — an action the model may take: search the web, run code, send a message
- **Agent** — a model in a loop: it plans, uses tools, checks the results, and tries again
- **MCP** — Model Context Protocol: a standard plug for connecting models to tools and data
- **RAG** — retrieval-augmented generation: look the facts up first, then answer
- **Skill** — a packaged recipe of instructions an agent loads for one specific job
- **Fine-tuning** — teaching a model your own examples so it specializes
- **Guardrails** — the checks around a model that keep its output safe and on-topic

---

## How the Pieces Fit Together

![anatomy](svg/lectures/ai/ai_everywhere/anatomy.svg)

---

## The Landscape

![landscape](svg/lectures/ai/ai_everywhere/landscape.svg)

---

## Software

- Assistants write, review, test, and document code alongside developers
- Agents fix bugs end-to-end: read the ticket, change the code, run the tests
- Legacy systems in COBOL and other old languages get translated to modern ones
- Half the industry's new code is now written with an AI in the loop
- And yet: software is just *one* industry on this tour — the rest are bigger

---

## Medicine

- AI reads X-rays, CT scans, and MRIs — flagging tumors radiologists can miss
- Early-warning systems watch vital signs and predict sepsis hours in advance
- Ambient scribes listen to the visit and write the clinical notes, giving doctors their evenings back
- Pathology slides are screened at a scale no human team could match
- Chat-based triage answers patient questions around the clock

---

## Drug Discovery and Biology

- AlphaFold predicted the 3D structure of essentially *every known protein* — 200 million of them
- That work won the 2024 Nobel Prize in Chemistry
- New proteins are now *designed* from scratch: enzymes, vaccines, materials
- AI-designed drug candidates have reached human clinical trials in years, not decades
- Cost of discovering a candidate molecule is collapsing

---

## Finance

- Fraud detection scores every card swipe on the planet in milliseconds
- Banks screen transactions for money laundering across billions of records
- Insurers settle simple claims automatically from photos and documents
- Analysts summarize earnings calls and filings the moment they are published
- Credit decisions weigh thousands of signals instead of three

---

## Law

- Contract review that took associates a week now takes an afternoon
- Discovery: AI sifts millions of emails and documents for the relevant few
- Legal research assistants cite the case law, not just summarize it
- Judges and firms use AI to draft, translate, and check filings
- The caution tale: lawyers sanctioned for citing hallucinated cases — guardrails matter

---

## Education

- Every student gets a patient, personal tutor that never runs out of time
- Khan Academy's tutor guides students to the answer instead of giving it away
- Language apps hold spoken conversations at exactly your level
- Teachers generate lesson plans, quizzes, and feedback in minutes
- Accessibility: material rewritten for any reading level on demand

---

## Scientific Research

- AI proposed 2.2 million new crystal structures — centuries of materials science in one shot
- It controls the plasma inside experimental fusion reactors in real time
- An AI solved International Math Olympiad problems at silver-medal level
- Literature assistants read thousands of papers so researchers start at the frontier
- Labs run robot experiments chosen by models, around the clock

---

## Climate, Weather, and Energy

- AI weather models forecast 10 days ahead — faster and often better than supercomputers
- Satellites plus AI spot wildfires and methane leaks within minutes
- Power grids balance solar and wind with AI demand prediction
- Data-center cooling bills cut by double digits through learned control
- Climate models downscaled to street-level flood risk

---

## Agriculture

- Smart sprayers see each plant and spray *only* the weeds — herbicide use drops by two thirds
- Drones and satellites monitor crop health across entire regions
- A phone photo of a leaf diagnoses plant disease in the field
- Dairy farms predict each cow's health and yield individually
- Harvest robots pick fruit judged ripe by vision models

---

## Manufacturing

- Cameras on the line catch microscopic defects at full production speed
- Machines report their own failures days before they happen
- Generative design invents parts lighter and stronger than human drafts
- Digital twins rehearse factory changes in simulation before touching steel
- Warehouse robots navigate, pick, and pack alongside people

---

## Transportation

- Robotaxis carry hundreds of thousands of paid passengers every week
- Delivery fleets shave millions of kilometers with AI-planned routes
- Cities retime traffic lights with AI and cut stop-and-go emissions
- Airlines predict maintenance, delays, and fuel burn per flight
- Ships route around weather chosen by learned models

---

## Space and Astronomy

- Exoplanets found by AI combing through telescope data humans had already searched
- Mars rovers pick their own science targets while out of contact
- AI stacks and sharpens telescope images — including the first photos of black holes
- Asteroid-hunting systems flag threats among millions of moving dots
- Satellite constellations dodge debris with automated maneuvers

---

## Art and Design

- Text-to-image models paint anything you can describe, in any style
- Designers storyboard, iterate, and explore in minutes instead of days
- Architects generate and compare building concepts before drawing one line
- Museums use AI to restore damaged works — even repainting the lost edges of a Rembrandt
- Fashion houses prototype collections virtually before cutting fabric

---

## Music

- AI separated John Lennon's voice from a noisy 1977 tape — the Beatles released the song in 2023
- Text-to-music services compose full songs with vocals from a sentence
- Mastering, once a studio luxury, is now an instant online service
- Musicians hum a melody and get a full arrangement back
- Streaming services compose your playlists — and detect AI fakes

---

## Film and Video

- Actors are de-aged by decades on screen — convincingly
- Dubbing now moves the actors' lips to match the new language
- Text-to-video models generate photoreal footage from a paragraph
- Studios restore and upscale century-old film frame by frame
- Effects that needed render farms now run on a laptop

---

## Writing, Journalism, and Translation

- News agencies auto-write thousands of earnings and sports reports per quarter
- Machine translation reached everyday-fluent quality in dozens of languages
- Live captions and subtitles appear as the speaker talks
- Editors use AI for fact-checking leads and taming document dumps
- Authors brainstorm, outline, and polish with a tireless first reader

---

## Gaming

- AI beat world champions at Go, poker, StarCraft, and Dota
- Game characters hold unscripted conversations with players
- Whole worlds — terrain, quests, dialogue — are generated procedurally
- Thousands of AI playtesters find the broken level before launch day
- Live anti-cheat models watch for inhuman behavior

---

## Sports

- Automated line calls officiate top tennis — and football offside decisions
- Every player movement is tracked; tactics are mined from the data
- Formula 1 teams run AI race strategy live during the race
- Training loads tuned per athlete to predict and prevent injury
- Broadcast highlights are clipped and narrated automatically

---

## Customer Service and Retail

- One retailer's assistant does the work of 700 human agents — with higher satisfaction
- Recommendation engines drive a third of e-commerce revenue
- Demand forecasting keeps shelves stocked and waste down
- Prices adjust to demand in real time across millions of items
- Voice bots handle bookings, returns, and routine calls end-to-end

---

## Accessibility

- Blind users point a phone at the world and hear it described in detail
- Live captions turn every conversation, lecture, and video into text
- People losing their voice to ALS bank it — and speak with it forever
- Sign language is translated to speech, and speech to sign
- Documents simplify themselves to any reading ability

---

## Archaeology and History

- Carbonized scrolls buried by Vesuvius in 79 AD are being read — without unrolling them
- AI restores missing letters in damaged ancient Greek inscriptions
- Hundreds of new Nazca desert figures found by scanning aerial imagery
- Cuneiform tablets are translated at a pace no human team could match
- Lost languages and faded manuscripts are next in line

---

## The Common Pattern

![pattern](svg/lectures/ai/ai_everywhere/pattern.svg)

---

## The Takeaway

- The raw material was always *data*: images, sound, text, sensor readings
- The model does one of four things: it sees, predicts, generates, or decides
- Humans stay in the loop where stakes are high — medicine, law, driving
- The dazzling part is not any single trick — it is the *same* trick working everywhere
- Pick your own field: start with a real weekly task, not with the technology
- Treat the model as a brilliant, overconfident intern: delegate, then verify
