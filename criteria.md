# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. 误判率

我自己写的 10 篇文章里，最多 1 篇被判为“很可能是AI写的”。

理由：被冤枉的作者会觉得这个功能很垃圾，还不如没有。在写作网站上，冤枉一个真人的代价，比漏掉一篇AI文章更大。

---

## 2. 分数差距
我选 3 篇明显AI写的、3 篇明显人写的文章。AI组的平均总分，要比人写组的平均总分至少高 0.5。

理由：差距要非常明显，否则系统分不清边界，标签就没有意义。


---

## 3. 不确定标签
我准备 10 篇人写后又被AI改过的文章，至少5篇要被判为“不确定”。

理由：有些优秀作者会写出很标准的文章，系统猜不准时，说“不确定”比冤枉人强。



## 4. 申诉有效
我测试 5 次申诉，5 次都要做到：状态变成 under_review，并且日志里多一条申诉记录。

理由：被冤枉的作者唯一的补救方式就是申诉。如果申诉没反应，他会更生气。


---

## 5. 坏输入
我测试 3 种坏输入：没有 text、text 是空白、text 超过 10000 个字符。3 种都要返回错误码 400 和一句说明问题的提示，系统不能崩溃。

理由：用户什么都可能交上来，系统一崩溃，所有人都用不了。





---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
