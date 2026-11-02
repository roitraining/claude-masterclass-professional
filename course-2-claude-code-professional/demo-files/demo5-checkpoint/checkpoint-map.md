# Demo 5 worksheet: where does a human checkpoint belong?

Read `nightly-fix-and-ship.yml`. Mark each step. Then compare with the instructor's answer.

| Step in the pipeline | Who acts | What can go wrong | Checkpoint here? |
|---|---|---|---|
| Schedule trigger at 03:00 | The schedule | Nothing starts that was not planned | |
| Claude fixes failing tests and moves dependencies | Claude, unattended | It can change a test so it passes instead of fixing the code | |
| Claude pushes to the branch | Claude | The branch is isolated from main | |
| Open the pull request and set it to merge itself | The workflow | The change reaches main with no person reading it | |
| Deploy to production after the merge | The workflow | An unreviewed change is live | |

Two questions to answer in the room:

1. Which one step lets an unreviewed change reach customers, and what is the cheapest checkpoint that stops it?
2. Which steps should NOT get a checkpoint, and why?
