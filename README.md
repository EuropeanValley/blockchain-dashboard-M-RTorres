[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/N3kLi3ZO)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23640601&assignment_repo_type=AssignmentRepo)
# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field | Value |
|---|---|
| Student Name | Germán |
| GitHub Username | MRTorres |
| Project Title | Blockchain Dashboard |
| Chosen AI Approach | Predictor, probably |

## Module Tracking

Use one of these values: `Not started`, `In progress`, `Done`

| Module | What it should include | Status |
|---|---|---|
| M1 | Proof of Work Monitor | Done |
| M2 | Block Header Analyzer | Done |
| M3 | Difficulty History | Done |
| M4 | AI Component | Done |

## Current Progress

Write 3 to 5 short lines about what you have already done.

- The four modules are done, althoug I would like to modify the AI Component a little to make it a little more readeble
- PD: It seems I forgot to push commit when I finished the module 4. Know that it was finished like a week ago. 
## Next Step

Write the next small step you will do before the next class.

- My intention was to add one of the three extra modules now at the last minute, but I just realiced I have to make a report, so I will do that instead.

## Main Problem or Blocker

Write here if you are stuck with something.

- No mayor Blockers

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```text
template-blockchain-dashboard/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- app.py
|-- api/
|   `-- blockchain_client.py
`-- modules/
    |-- m1_pow_monitor.py
    |-- m2_block_header.py
    |-- m3_difficulty_history.py
    `-- m4_ai_component.py
```

<!-- student-repo-auditor:teacher-feedback:start -->
## Teacher Feedback

### Kick-off Review

Review time: 2026-04-29 20:31 CEST
Status: Amber

Strength:
- I can see the dashboard structure integrating the checkpoint modules.

Improve now:
- M1 still needs clearer evidence of a working Proof of Work monitor in the dashboard.

Next step:
- Turn M1 into a working dashboard view with live Proof of Work metrics, not just a placeholder.
<!-- student-repo-auditor:teacher-feedback:end -->
