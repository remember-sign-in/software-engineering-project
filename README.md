# software-engineering-project
    记得签到

## 组员
    钟贤杰 
    林少涵
    周建辉
    范嘉诚
## 仓库配置
    仓库包含两个特殊分支
    · dev 开发分支
        用于合并最新的开发代码
    · main 生产分支
        用于存储生产代码

  我们的工作流是：个人开发时由dev分支checkout出来一个新分支例如zxj--dev，开发结束后通过代码互审合并到dev分支，完成某一整块的功能后，将dev分支合并到main分支，并使用github的release功能发布一个新的版本
 
## 开发工作流
    ~ 在需求分析、任务分解结束后，将一个大块的功能分成若干小的、可以单人实现的小功能，这些小功能通过Github中的Issue功能分配给特定的开发人员
    ![Alt text](md_img\image.png)
    
    （注）issue的标签size用于设定工作量

## Pull Request
    ~ 在开发人员完成某个Issue的需求后，可以利用Github的Pull Request功能提出代码复审、合并分支的请求，合并到dev中需要1个人复审，合并到main中需要两个人复审

    ~ 提交的Pull Request包含以下要求：
        · 填写实现功能的描述
        · 分配Reviewers，提醒他们审核你的Pull Request
        · 在描述文本框中，输入close #IssueID，可以自动将该PR与Issue关联，当PR被合并后，Issue自动关闭

## 代码复审
    ~ 作为代码复审的人员，通过点击File changed标签页，审核开发人员修改的代码，对其代码提出评论，当认为其通过审核后，在评论中选择Approve，当Approve的人数达到分支保护规则的要求时，就能够合并分支了

    ~ 在合并时，Github会自动检测有无冲突，如果有冲突，会要求Resolve conflicts，Github提供了解决冲突的页面，点击Resolve conflicts按钮可以直接在Github网站中解决冲突，提交commit

    ~ 在冲突解决、代码复审完成后，merge的按钮被允许点击，可以使用Squash and Merge的选项，将这个分支内的所有commit压缩成一个commit进行合并
