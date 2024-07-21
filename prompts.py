flashcard_prompt = '''
Take the transcript of this educational video given and provide back a list of flashcards based on the transcript 
as a list of dictionaries in json. The output should follow the following pattern: 
{
    flashcards: 
    [
        {
            title: main idea as a one sentence summary,
            details: one paragraph explaining the idea in detail
        }
    ]

}
Do not return back any text besides the json output
'''


bullet_point_prompt = '''
Take the transcript of this educational video provided  and provide back a list of bullet points based on the transcript 
as a list of strings in json. The bullet points should not include any personal information about indivudals in the video, 
rather it should only describe the content trying to be explained. The output should follow the following pattern: 
{
    bullet_points: 
    [
        main idea number one in great detail,
        main idea number two in great detail
    ]
}
Do not return back any text besides the json output

'''


quick_read_prompt = '''
You are an academic journal writer that makes content for educational use. You are using the culmination of the data provided
to provide a quick read of 1000 words on this topic. Write the essay with the following information as context. The response will be in json. First a title is declared which will be the main topic of the paper.
The essay should have The first paragraph should provide an overview over what the topic is. The middle paragraphs should go into detail over the main points of the context.
The final paragraph should summarize the findings. The output should follow the following pattern:

{
    title: Topic of paper,
    paragraphs: [paragraph1, paragraph2...]
}
Do not return back any text besides the json output
'''
