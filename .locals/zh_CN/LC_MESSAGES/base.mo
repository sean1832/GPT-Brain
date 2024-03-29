��    K      t  e   �      `     a     {     �  
   �     �  3  �     �     �                  
   "  	   -  &   7     ^     x     �    �     �	     �	  	   �	     �	  '   �	     
     
     0
     C
    O
     d  
   p     {     �  '   �  !   �  
   �     �     �  
   �               "     *     9     K     W     m     v     �  �   �  �   �  �   O     �        1     Q   E     �     �  �   �     �  
   �     �  	   �     �  	   �  
   �     �               '     3     D     M     Y     f    t     �     �  	   �     �     �  W  �     /     N     [     l     s     �     �     �     �     �       �                  !     .     ;     Z  #   g     �     �  #  �     �     �     �       $   	     .     M     Z     j     w  "   ~     �     �     �     �  	   �     �                 �   4  �     �   �     0     =  J   M  5   �     �     �  �   �     �     �     �     �     �  	   �  
          
        &     =     T  
   e  
   p     {     �     $      &                      B             '      "   0   !   G       .                    F   (                         E         
      >      :       K   D           6   ?   +   A      5       C   %                     I   <               3          2   7             H   4         	   J   /   ;   #   =           *      ,       )   9              -       @   8   1    #### Directory to Exclude ) if you find any. API Keys Add Filter Advanced Options An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

It is generally recommend altering this or `temperature` but not both. Answer count Append Mode Ask Brain:  Author Brain Updated! Chunk size Clear Log Combinations of operations to perform. Configuration of prompts. Configure your OpenAI API keys. Create Decreasing the model's likelihood to repeat the same line verbatim. Penalize new tokens based on their existing frequency in the text so far.

[See more information about frequency and presence penalties.](https://platform.openai.com/docs/api-reference/parameter-details) Delete Filter Delete Prompt Delimiter Directory Filter Enter file or directory name to exclude Force Delimiter Frequency penalty Frontmatter Filter Github Repo Larger the number increasing the model's likelihood to talk about new topics. Penalize new tokens based on whether they appear in the text so far.

[See more information about frequency and presence penalties.](https://platform.openai.com/docs/api-reference/parameter-details) Log Cleared Max Tokens Menu Model Model used for answering user question. Modify your brain knowledge base. New Prompt New Prompt Name Note Directory Operations Presence penalty Prompt File Prompts Question Model Raw Memory Inputs Report bugs Select Note Directory Settings Stream (experimental) Temperature The maximum number of tokens to generate in the completion.

The token count of your prompt plus `max_tokens` cannot exceed the model's context length. Most models have a context length of 2048 tokens (except for the newest models, which support 4096). The number of answers to generate. The model will continue to iteratively generating answers until it reaches the answer count.

Note that this function does not supports `stream` mode. The number of tokens to consider at each step. The larger this is, the more context the model has to work with, but the slower generation and expensive will it be. Thinking on  Thinking on Answer This is a beta version. Please [🪲report bugs]( This is my personal AI powered brain feeding my own Obsidian notes. Ask anything. Updating Brain... Version What sampling temperature to use, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. 

It is generally recommend altering this or `top_p` but not both. my-info new_prompt question summarize ✅File saved! ❌Delete 💬Answer 💽Brain Memory 💾Save 📁Select Note Directory 📝Prompts 📥download log 📩Send 🔄Refresh 🔑API Keys 🧠GPT-Brain Project-Id-Version: 
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2023-02-23 02:32+1100
Last-Translator: 
Language-Team: 
Language: zh_CN
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Generator: Poedit 3.2.2
 #### 需要过滤的目录 )。 API密匙 增加筛选 高级设置 一种替代温度采样的方法被称为“核心采样”，在该方法中，模型会考虑到具有 top_p 概率质量的标记的结果。因此，当 top_p 的值为 0.1 时，只有包含前 10% 概率质量的标记会被考虑。

通常建议调整此参数或`温度`参数中的其中一个，但不能同时调整两个参数。 回答数量（Answer count） 附加模式 提问大脑：  作者 大脑已更新！ 区块大小（Chunk size） 清除日志 执行的操作组合。 这里设置咒文（prompt） 这里设置OpenAI API密匙。 创建 降低模型重复相同句子的可能性。基于文本中已有的词频来惩罚新的令牌。

[有关频率和存在程度惩罚的更多信息，请参见此处（英文）](https://platform.openai.com/docs/api-reference/parameter-details) 删除筛选 删除咒文 分界符号 目录过滤 输入需要排除的目录名 强制分界 频率惩罚（Frequency penalty） 前置筛选 Github源代码 增加数值会使模型谈论新话题的可能性增加。基于词语出现的频率和存在程度对新的令牌（token）进行惩罚。

[有关频率和存在程度惩罚的更多信息，请参见此处（英文）](https://platform.openai.com/docs/api-reference/parameter-details) 日志以清除 最大令牌数（Max Token） 菜单 模型 回答用户问题的语言模型。 这里修改大脑知识库... 新建咒文 新建文件名 笔记目录 操作 存在惩罚（Presence penalty） 咒文文件 咒文（Prompts） 问题模型 笔记数据内容 报告bug 请选择笔记文件目录 设置 串流模式 温度（Temperature） 生成需要的最大数量的令牌数量。

你的咒文（prompt）和结果加起来不能超过模型的总长度。大多数模型的总长度限制为2048个令牌（最新的模型支持4096个）。 需要生成的答案数量。模型会不断迭代生成答案，直到达到所需答案数量。

注意此功能不支持`串流模式`。 增加数值会增加AI思考的令牌数量。这个数字越大，模型就有越多的上下文可用，但生成速度会更慢，而且成本更高。 正在思考 思考答案中 该版本为BETA测试版。如果遇到BUG，请[🪲在此处报告BUG]( 这是我的个人AI知识管理库，请随意问。 更新大脑中... 版本 使用什么采样温度，在0和1之间。较高的值如0.8会使输出更加随机，而较低的值如0.2会使它更加集中和确定。

一般建议改变这个值或`top_p`，但不能同时改变。 我的背景 新建咒文 问题 总结 ✅文件以保存！ ❌删除 💬回答 💽脑记忆 💾保存 📁选择笔记目录 📝咒文（prompt） 📥下载日志 📩发送 🔄刷新 🔑API 密匙 🧠GPT-大脑 