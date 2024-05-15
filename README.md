This study is important because there are many large and complex methods that were never changed. similarly, there were many small, and readable methods that changed many times. This means changes can happen for many other unknown factors. This makes prediction a very difficult job. But what we can do is learn from the majority of cases. What are good and what are ugly methods?

 RQ 0) Which age should we select for age normalization? (part of methodology)

 RQ 1) Does it follow 80-20 rule (or what percent of methods (x%) are liable for 80% revisions) --- the ugly methods
 
 RQ 2) What fractions of bugs are contained by these ugly methods?
 
 RQ 3) Are these x% methods the top x% in size? In that case, sorting with size would give us those methods. Or are the other code metrics perform better?

 RQ 4) If not, what are the charateristics of these methods?
    --- let's make two other groups (changed at least once (bad), never changed (good))
    --- how are the ugly methods different with the good and bad methods? Specially, what are the distinct characteristics in the ugly and the good methods. 
    --- do changes in ugly methods happen in bursts, or they are will distributed across times (entrophy).. how do the clusters look like when applied with         KSc clustering? 
    
RQ 5) Is it possible to predict ugly methods?
   
RQ 6) If not, then select 100 ugly methods.  Then find 100 good methods that have similar characteristics to the 100 ugly methods. Now, manually analyze, why these two sets have different change-proneness, although they have similar code characteristics. 
    --- who wrote this method, vs who wrote the good methods. what's their experiences, and contributions to the projects. or were there too many developers for those methods? 
