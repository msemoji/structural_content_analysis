# structural_content_analysis
This Python 3 and Jupyter codebase enables the description and representation of text such as of a tweet based on its document structure and content structure. The document structure is the order of specific content types and the number of sequential elements per content type.
  
<p>With this code, structural content analysis can be done on a group of text or by user to examine and compare common document structure and content structures eventhough the individual tweet text itself varies.

<p> For example a sample tweet could be: RT @someuser @anotheruser This is a cool idea @user1 to analyze a 📄 with a 💻😀! http:someurl.com
<p> The following document structure will be generated from this code:<br>
  [('RT',1),('at_mention',2),('text',5),('at_mention',1),('text',3),('emoji',1),('text',2),('emoji',2),('punctuation',1),('url',1)]
<p> And the content structure:<br>
  ['RT','at_mention','text','at_mention','text','emoji','text','emoji','punctuation','url']
 
<p>In addition you can get the spans of content for a specific content type, e.g.:<br>
  For at_mentions: [(@someuser,@anotheruser),(@user1,)]<br>
  and for emojis: [(📄,),(💻,😀)]
  
  
  
  
