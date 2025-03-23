from openai import OpenAI
import time


# establish client object.
client = OpenAI(api_key='ADD-KEY')

# timer used for latency performance only.
start_time = time.time()

def get_openai_response(prompt: str, system_prompt: str) -> str:
    """
    Simple chat method to provide the relevant document section as context to provide a answer to the user question.
    """
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ])

    return response.choices[0].message.content


# TODO: Could improve using few shot prompting to structure generated answers.
system_prompt = """
You are a helpful assistant. Your job is to answer the Question provided given the Context. 
Keep negative values if the relevant answer is negative as this could indicated losses or a decrease
If you are not sure on the answer return 'Unsure' and do not make a guess.
"""

user_question = input("What is your question?\n")

# TODO: Replace this with simple lookup to return 'closest matches' content from 'test_section_finder.py'.
# Content hardcoded below to independently test the effectivness of this sub-process as described in README.md.
relevant_content = """"table": [
                            [
                                "",
                                "2002",
                                "2001",
                                "2000"
                            ],
                            [
                                "net sales",
                                "$ 5742",
                                "$ 5363",
                                "$ 7983"
                            ],
                            [
                                "cost of sales",
                                "4139",
                                "4128",
                                "5817"
                            ],
                            [
                                "gross margin",
                                "$ 1603",
                                "$ 1235",
                                "$ 2166"
                            ],
                            [
                                "gross margin percentage",
                                "28% ( 28 % )",
                                "23% ( 23 % )",
                                "27% ( 27 % )"
                            ]
                        ],
                        "amt_pre_text": "in a new business model such as the retail segment is inherently risky , particularly in light of the significant investment involved , the current economic climate , and the fixed nature of a substantial portion of the retail segment's operating expenses . results for this segment are dependent upon a number of risks and uncertainties , some of which are discussed below under the heading \"factors that may affect future results and financial condition.\" backlog in the company's experience , the actual amount of product backlog at any particular time is not a meaningful indication of its future business prospects . in particular , backlog often increases in anticipation of or immediately following new product introductions because of over- ordering by dealers anticipating shortages . backlog often is reduced once dealers and customers believe they can obtain sufficient supply . because of the foregoing , backlog cannot be considered a reliable indicator of the company's ability to achieve any particular level of revenue or financial performance . further information regarding the company's backlog may be found below under the heading \"factors that may affect future results and financial condition.\" gross margin gross margin for the three fiscal years ended september 28 , 2002 are as follows ( in millions , except gross margin percentages ) : gross margin increased to 28% ( 28 % ) of net sales in 2002 from 23% ( 23 % ) in 2001 . as discussed below , gross margin in 2001 was unusually low resulting from negative gross margin of 2% ( 2 % ) experienced in the first quarter of 2001 . as a percentage of net sales , the company's quarterly gross margins declined during fiscal 2002 from 31% ( 31 % ) in the first quarter down to 26% ( 26 % ) in the fourth quarter . this decline resulted from several factors including a rise in component costs as the year progressed and aggressive pricing by the company across its products lines instituted as a result of continued pricing pressures in the personal computer industry . the company anticipates that its gross margin and the gross margin of the overall personal computer industry will remain under pressure throughout fiscal 2003 in light of weak economic conditions , flat demand for personal computers in general , and the resulting pressure on prices . the foregoing statements regarding anticipated gross margin in 2003 and the general demand for personal computers during 2003 are forward- looking . gross margin could differ from anticipated levels because of several factors , including certain of those set forth below in the subsection entitled \"factors that may affect future results and financial condition.\" there can be no assurance that current gross margins will be maintained , targeted gross margin levels will be achieved , or current margins on existing individual products will be maintained . in general , gross margins and margins on individual products will remain under significant downward pressure due to a variety of factors , including continued industry wide global pricing pressures , increased competition , compressed product life cycles , potential increases in the cost and availability of raw material and outside manufacturing services , and potential changes to the company's product mix , including higher unit sales of consumer products with lower average selling prices and lower gross margins . in response to these downward pressures , the company expects it will continue to take pricing actions with respect to its products . gross margins could also be affected by the company's ability to effectively manage quality problems and warranty costs and to stimulate demand for certain of its products . the company's operating strategy and pricing take into account anticipated changes in foreign currency exchange rates over time ; however , the company's results of operations can be significantly affected in the short-term by fluctuations in exchange rates . the company orders components for its products and builds inventory in advance of product shipments . because the company's markets are volatile and subject to rapid technology and price changes , there is a risk the company will forecast incorrectly and produce or order from third parties excess or insufficient inventories of particular products or components . the company's operating results and financial condition have been in the past and may in the future be materially adversely affected by the company's ability to manage its inventory levels and outstanding purchase commitments and to respond to short-term shifts in customer demand patterns . gross margin declined to 23% ( 23 % ) of net sales in 2001 from 27% ( 27 % ) in 2000 . this decline resulted primarily from gross margin of negative 2% ( 2 % ) experienced during the first quarter of 2001 compared to 26% ( 26 % ) gross margin for the same quarter in 2000 . in addition to lower than normal net .",
                        "amt_post_text": "." """

# structure prompt
prompt = f""" Question: {user_question} \
                Context: {relevant_content}
                    """

response = get_openai_response(prompt, system_prompt)
print(response)

# Example Q for hardcoded content: What is the percentage change in net sales from 2000 to 2001?

# Timings used for latency assessment only.
end_time = time.time()
print(f"time taken: {end_time - start_time}")