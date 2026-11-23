# COMP 440 HW3 write-up

Name:Shaylee O'Grady

Type each answer after the `>` under its question. An answer can run over several lines, but a blank line
ends it: to start a new paragraph, put a line with just `>` between the two. In a table, fill every cell
of every numbered row. Claude may paste a program's output where a question asks for it, but never an
answer. The homework page ticks a step when every answer in its section is filled in.

## Learning goals

In this homework you will:

- Understand what makes a program an *agent*. You will study a language model that picks the next Wikipedia search query, reads the page that comes back, and decides when to stop.
- Gain hands-on experience with the loop around the model by writing it yourself: its tools, its instructions, and its limit of 12 lookups.
- Compare the agent with two simpler methods on your claims, and measure how effective each one is.
- Check the agent's evidence yourself, and decide whether accuracy alone is a fair measure of it.

For extra credit, in Part 3, you find out why the agent fails on your claims, make one change, and see where Wikipedia, which is written by its volunteer editors, is thin, out of date or wrong.

# Part 0: Set up and check one claim

## 0a. Get your copy running

There is nothing to write for this step except your name, after `Name:` at the top of this file.

## 0b. Ask the model to assess a claim without tools

What verdict did the model give (*supported*, *refuted* or *doesn't say*), and what reason did it give? Quote the lines of the output that show them.

> The model gave a verdict of "doesn't say." The model's reasoning was "I can't confirm from memory that English Wikipedia has an article on "Persian Surgery Dervishes" identifying its composer or giving that composer's birth date, so I can't verify the claim either way."

## 0c. Give it one search

Which Wikipedia page did it read? Quote the line of the output that shows it.

> Page: Persian Surgery Dervishes

Persian Surgery Dervishes is a recording of two live solo electric organ concerts, the first held in Los Angeles on 18 April 1971 and the second in Paris on 24 May 1972, by the avant-garde minimalist composer Terry Riley, following his A Rainbow in Curved Air and In C.

Sections: Background and release, Music, References, External links

Did that page settle the claim correctly? If not, why do you think the search led there?

> The page did not settle the claim correctly, and I believe that is because the top page may have more general knowledge about the recording, but was not yet specific enough to get to the answer of the composers birthday. One page is not enough to get the answer. 

## 0d. Run the agent and read its trace

In one or two sentences, how did the agent get from the claim to its verdict? Point to the trace entries by their numbers.

> It searched a singular query, and then from the results of that search read the wikipedia page called "Terry Riley". Meanwhile after it's search it went to a seperate database called Wikidata to search Terry Riley and date of birth. Then lastly decided it's verdict once it saw both it's sources answer's matched, and quoted evidence from the page as evidence.

Which lookup would you have done differently, and how? If none, which one surprised you?

>I would have done the search one differently, because it is so vague, so it doesn't get to the answer as effectively. If the inital query was better, I think it would be more efficient of a process. 

Describe Wikidata briefly. Why may it be important to this task?

>It's a seperate database for one property of one entity. So it may be important to this task, because it can find the answer from a singular property of a singular entity. 

# Part 1: How the agent works

## 1a. Design the loop

Your loop should repeatedly call the model with the message history so far, and ask for its next step. It should check whether the model has given an answer yet. If not, it should make the lookups that step asks for, and add what they return to the history. It should also pay attention to whether the loop has reached its limit: a claim that runs out of lookups cannot be decided. One limit is set for you: 12 lookups for a claim.

The Background and an example outline are under 1a on the homework page, and in [instructions/part1.md](instructions/part1.md#1a-design-the-loop).

Write your outline of the loop in the code block: what it remembers, what it repeats, and every way it stops.

```
The loop should keep track of how many Wikipedia lookups it has made, with a maximum of 12. It should repeatedly ask the LLM what to do next using the conversation history so far. If the LLM asks for more information, the loop should look it up on Wikipedia, add the results to the conversation history, and ask the LLM again. It should keep repeating this process until the LLM gives a final answer or reaches the limit of 12 lookups. Once it has made 12 lookups, it should ask the LLM one final time to see if it can give an answer using the information it has. If the LLM gives an answer, the loop should stop and return it. If it asks for more lookups, the loop should stop without giving a verdict. It should never ask the LLM again after that final attempt.
```

List each thing your loop remembers from one turn to the next, and say what would go wrong without it.

> My loop remembers the conversation history, including the model's replies and Wikipedia search results, so it doesn't lose track of what it has already learned or repeat searches. It also keeps count of how many lookups it has made out of 12 so it knows when to stop. Without these, the agent could lose important information or keep searching past the limit and take a long time to reach a verdict.

Now open `reference_loop.py` and compare it with your loop. Describe one difference in implementation and the resulting effects on agent behavior.

> In the reference loop, the agent checks whether it has reached the limit before making more lookups. In my loop, the agent makes the requested lookups and then gives the model one final chance to answer. This means the reference loop could stop before the model gets to use the latest search results, while my loop gives it a chance to use everything it has found. (difference in order of the loopup limit)

## 1b. Be the agent

The claim: "Vic & Anthony's Steakhouse is located at the American casino that was combined with the California Club. The casino is owned by Landry's, Inc."

List your lookups, in order. Ask Claude to paste every column but the last from `runs/part1/lookups.jsonl`. Type "Why you chose it" yourself.

| # | Tool | What you asked for | Why you chose it |
|---|---|---|---|
| 1 | search | Vic & Anthony's Steakhouse Landry's Inc |Needed sources to pull evidence from and can't find those before searching. |
| 2 | read | Vic & Anthony's Steakhouse |reading the searches best results |
| 3 | read | Landry's |reading the searches best results |
| 4 | search | Vic & Anthony's in American casino |Wasn't fully confident from earlier results, so needed to search more to get full answer.|
| 5 | read | Vic & Anthony's Steakhouse |Read results to gather information to get verdict |
| 6 | read | Golden Nugget Lake Charles |Read results to gather information to get verdict |

What is your verdict on the claim, and which sentence or sentences from what you read is it based on?

> Verdict : Supported; Evidence: Page: Vic & Anthony's Steakhouse Vic & Anthony's is an American steakhouse restaurant chain with locations in Downtown Houston, and inside the Golden Nugget Casinos in Las Vegas, Atlantic City and Lake Charles. Vic & Anthony's is owned and operated by Landry's, Inc.

## 1c. Watch the agent work

List the three traces you read closely. At least one should be a claim the agent got wrong (if it got any wrong).

| # | Claim (first few words) | Articles | Did it match the dataset's label? | Did it get there for a good reason? Why or why not |
|---|---|---|---|---|
| 1 |"the rule of the dynasty that was active when the stone was inscribed.."|3|yes; supported |It did, it had three very supportive articles pulled, and even discussed a misleading point in it's explaination. |
| 2 |"Four operas are amoung the artist who composed The Prelude for Clarinet..." |2|no;refuted|The agent's explanation gives two reasons, not one. First, the list of best-known works it quoted names no operas. Second, the page says "five operas", not four. Its evidence is one quoted passage, from the "Krzysztof Penderecki" page, which it read in entry 3. It did 3 lookups in all.|
| 3 |"The former leader of the school of Soviet and Russian humorists's youngest son.."|2|no;supported|Its explanation says: "The articles never use the words 'youngest son,' but they mention only one son (Konstantin, alongside a daughter, Ekaterina), so the claim holds in substance though that detail is not stated explicitly." So, again it's being too specific maybe?|

Which trace did you find most interesting, and what did the agent do well or badly in it?

> I find the last one form above the most intresting, because it used some intresting reasoning (the daughter being the only other child mentioned) to feel like the claim was supported. 

## 1d. Write the agent's instructions

What changed in the agent's traces after you wrote your instructions? Give one claim as an example.

> 2 rows changed one that was originally an incorrect verdict became correct and the second one with the claim "The quartets that released One Thousand Years of Trouble and Vector were both a rock band." Went from a semi correct verdict "doesn't say" to a more confindent verdict of "refuted".

## 1e. Start the full run, and predict

Predict the share of claims each version will get right (its verdict matches the dataset's label), as a percentage. A guess is fine; the reasons are what I grade.

| Version | 2 articles | 3 articles | 4 articles | Why you think so |
|---|---|---|---|---|
| No tools |25|15|10|It has no tools so it's already getting a large portion wrong, then the more articles needed the harder the question so it decreases in percents|
| One search |55 |45|25 |It has only a singular search, so it going to be closer to a 50/50 chance now that it has some context, but similarly to before it will struggling with claims that require more information|
| Agent |86|80|65|Agent can use many sources, but I already saw it struggle to be entirely correct, so I assume it will be pretty strong in on claims that require 2-3 articles but have a larger drop off of accuracy for claims that need 4 articles |

How many lookups will the agent make per claim, on average? Why?

> 7 Because it has a rule that it can't go over 13 so I would think it would be around this middle range. 

# Part 2: The agent against the baselines

## 2a. Compare accuracy

Ask Claude to paste the report of your full run, from `runs/part2/report.txt`, into the empty block below.

```
Share of claims where the verdict matched the label:

                          no-tools  one-search       agent
HoVer, 2 articles         19/34       16/34       22/34   
HoVer, 3 articles         23/33       17/33       21/33   
HoVer, 4 articles         19/33       17/33       20/33   
All                       61/100      50/100      63/100  

HoVer, supported          16/50        1/50       24/50   
HoVer, not supported      45/50       49/50       39/50   

Average per claim:

                         lookups   seconds
no-tools                     0.0       3.4
one-search                   2.0       4.3
agent                        5.1      12.1

1 runs gave no verdict (for example a refusal, or out of lookups). They count as wrong. The results viewer lists them on this run's page, under "Claims with no verdict, or that stopped with an error".
```

How do the results compare with your predictions? Where were you furthest off? Use the numbers from your run, by number of articles.

>

Does the gap between the agent and the one-search baseline grow with the number of articles? What in the claims or the traces explains what you see?

>

The no-tools baseline read nothing. How did it do, and what does that tell you about these claims?

>

## 2b. Check the evidence yourself

Fill in one row for each of the first five claims in your full run, in the order of the claims file, where the agent's verdict is *supported* or *refuted*.

| # | Claim (first few words) | Agent's verdict | Matched the dataset's label? | Does the quoted evidence support that verdict? | Why or why not |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

Of the five, how many matched the dataset's label, and for how many of those does the quoted evidence support the verdict?

>

Is accuracy alone a good measure of this agent? Why or why not?

>

# Part 3 (extra credit): Why the agent fails, and one change

## 3a. Sort the failures

Fill in one row for each of the first eight failures in your full run, rows 1 to 8 of the claims table for runs/part2 with "Result" in "The agent" box set to "does not match the dataset's label (any reason)". If you have fewer than eight, fill a row for each and delete the rest.

| Row | Claim (first few words) | Your label | The entry of the trace that shows it | Is the dataset's label right? (yes, no or can't tell) | Claude's label |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |

Where did you and Claude disagree, and who do you think is right?

>

Which kind of failure was most common? If no kind repeats, say which failure you will aim at in 3b, and why.

>

## 3b. Make one change

What did you change, and why did you expect it to help?

>

How many of your evaluation claims did the agent match before the change and after it? Which of your failures from 3a now match?

>

Quote one claim the agent matched before the change and not after it, if there is one, and say what you think happened. If there is none, say so.

>

## 3c. Write it up

What does the agent's loop add over one search, what does it cost, and when would you not use an agent for a job like this? Use your numbers from Part 2 and Part 3.

>

What did your claims show you about Wikipedia as a source? Where it was thin or wrong, why might that be, given who writes it?

>

Your numbers rest on 100 claims. Which of your conclusions would you trust on another 100 claims, which might be chance, and what would you measure to find out?

>
