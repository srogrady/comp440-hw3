"""Your agent's loop, which you design in step 1a. The homework page says what the
loop is for, under "1a. Design the loop" (also in instructions/part1.md), and the
check tells you each rule it must follow when your loop breaks it.

You design the loop as an outline in plain words, in WRITEUP.md under 1a. The
loop below the line that says where it goes is Claude's translation of that
outline, written with the parts in loop_parts.py: each line of your outline is a
comment, with about one line of Python for it under it. To change the loop,
change your outline and ask Claude to translate it again.

Check it after each translation. The check uses a scripted stand-in for the
model and for Wikipedia, so it needs no key and costs nothing:

    uv run python check_loop.py

Part 0 runs the agent on the reference loop. Once every rule passes, the agent
runs on this loop and no other: the runs of 1c and later need it to pass.
"""

import anthropic

# The names below include every one the file had before the parts, so that a loop written
# then still runs.
from agent import (ACCEPTED, DECLINED, INSTRUCTIONS, MAX_REJECTED, MAX_STEPS, MODEL, NO_ANSWER,
                   OUT_OF_STEPS, RAN_OUT, REJECTED, REJECTED_TOO_OFTEN, REMINDED, REMINDER,
                   TOOLS, answer_problem, clean_answer, finish, run_tool)
from loop_parts import Conversation


def run_agent(claim, client=None, max_steps=MAX_STEPS, lookup=run_tool):
    """Check one claim. Returns what talk.accept() or talk.stop() returns."""
    client = client or anthropic.Anthropic()
    system = INSTRUCTIONS.read_text()
    messages = [{"role": "user", "content": f"Claim: {claim}"}]
    trace, read_so_far = [], []
    talk = Conversation(claim, client, system, messages, trace, read_so_far, lookup)
    steps = 0          # lookups made so far
    rejected = 0       # answers sent back so far

    # Your loop should repeatedly call the model with the message history so far, and ask for
    # its next step. It should check whether the model has given an answer yet. If not, it should
    # make the lookups that step asks for, and add what they return to the history. It should
    # also pay attention to whether the loop has reached its limit: a claim that runs out of
    # lookups cannot be decided.
    # ---- your loop goes below this line (step 1a) ----
    # The loop should keep track of how many Wikipedia lookups it has made, with a maximum of 12.
    # (steps, set up above, is this count; max_steps is the maximum of 12)
    # It should repeatedly ask the LLM what to do next using the conversation history so far.
    while True:
        reply = talk.ask()
        # If the LLM asks for more information, the loop should look it up on Wikipedia, add the
        # results to the conversation history, and ask the LLM again.
        if reply.lookups:
            for call in reply.lookups:
                talk.give(call, talk.run(call))
                steps += 1
            talk.send_results()
        # It should keep repeating this process until the LLM gives a final answer or reaches the
        # limit of 12 lookups.
        if reply.answer is not None:
            return talk.accept(reply.answer, steps)
        if steps >= max_steps:
            break
    # Once it has made 12 lookups, it should ask the LLM one final time to see if it can give an
    # answer using the information it has.
    reply = talk.ask()
    # If the LLM gives an answer, the loop should stop and return it.
    if reply.answer is not None:
        return talk.accept(reply.answer, steps)
    # If it asks for more lookups, the loop should stop without giving a verdict.
    if reply.lookups:
        return talk.stop(RAN_OUT, steps)
    # It should never ask the LLM again after that final attempt.
    # (no new Python: both lines above stop the loop, and nothing after them asks again)
