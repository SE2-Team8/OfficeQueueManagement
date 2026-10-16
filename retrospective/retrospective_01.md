TEMPLATE FOR RETROSPECTIVE (Team ##)
=====================================

The retrospective should include _at least_ the following
sections:

- [process measures](#process-measures)
- [quality measures](#quality-measures)
- [general assessment](#assessment)

## PROCESS MEASURES 

### Macro statistics

- The number of stories committed and done by the team were both 2
- The team committed and completed 6 story points
- Hours of work estimated vs actually spent: 40h 30m vs 36h 5m

**Remember**  a story is done ONLY if it fits the Definition of Done:
 
- Unit Tests passing
- Code review completed
- Code present on Git
- End-to-End tests performed

> Please refine your DoD 

### Detailed statistics

| Story  | # Tasks | Points | Hours est. | Hours actual |
|--------|---------|--------|------------|--------------|
| _#0_   |    8    |    -   |    20h 30m |   15h 50m    |
| n. 1   |    5    |    3   |   10h      |    11h 15m   |
| n. 2   |    5    |    3   |    10h     |     9h       |
   

> place technical tasks corresponding to story `#0` and leave out story points (not applicable in this case)

- Hours per task average, standard deviation (estimate and actual)

|            |  Mean  | StDev |
|------------|--------|-------|
| Estimation |  2.250 | 2.005 | 
| Actual     |  1.801 | 1.885 |

- Total estimation error ratio: sum of total hours spent / sum of total hours effort - 1: `-0.11`

    $$\frac{\sum_i spent_{task_i}}{\sum_i estimation_{task_i}} - 1$$

- Absolute relative task estimation error: sum( abs( spent-task-i / estimation-task-i - 1))/n: `0.30`

    $$\frac{1}{n}\sum_i^n \left| \frac{spent_{task_i}}{estimation_task_i}-1 \right| $$

## QUALITY MEASURES 

For the first sprint, the team didn't keep track time separately for unit and E2E testing. This is a problem that will be fixed
in the next sprint.

- Testing:
  - Total hours estimated: 10h
  - Total hours spent: 11h
  - Number of test cases: ?
  - Coverage: 100% (pytest results below)


- Unit Testing:
  - Total hours estimated: 
  - Total hours spent
  - Nr of automated unit test cases 
  - Coverage
- E2E testing:
  - Total hours estimated
  - Total hours spent
  - Nr of test cases
- Code review 
  - Total hours estimated 
  - Total hours spent  


## ASSESSMENT

- What caused your errors in estimation (if any)?

- What lessons did you learn (both positive and negative) in this sprint?

- Which improvement goals set in the previous retrospective were you able to achieve? 
  
- Which ones you were not able to achieve? Why?

- Improvement goals for the next sprint and how to achieve them (technical tasks, team coordination, etc.)

> Propose one or two

- One thing you are proud of as a Team!!


---
### Pytest coverage results
|Name|                                          Stmts|   Miss|  Cover|
|----|-----------------------------------------------|-------|-------|
|tests\conftest.py|                                12|      0|   100%|
|tests\integration\test_next_customer_api.py|      45|      0|   100%|
|tests\integration\test_ticket_api.py|             61|      0|   100%|
|tests\unit\test_get_ticket.py|                    36|     0|   100%|
|tests\unit\test_get_ticket_wb.py|                 12|      0|  100%|
|tests\unit\test_next_customer.py|                 43|      0|   100%|
|tests\unit\test_next_customer_wb.py|             116|      0|   100%|
|tests\unit\test_schemas.py|                       26|      0|   100%|
|TOTAL|                                           351|      0|   100%|