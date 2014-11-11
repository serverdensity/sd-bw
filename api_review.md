subjectId - it's a bit unclear how to get that perhaps from the API docs. Can this be renamed deviceId. It might make more sense. 

the tree seems a bit redundant. Can you take that away somehow? 

Spelling error in example it should be 'rxMByteS' instead of 'rxMBytesS'


What about errors. If you don't get a 200 status code what does the output look like then?

{
    "message":"Invalid token",
    "errors":[
        {"type":"invalid_token","subject":"token"}
    ]
}

Gives you a dictionary with a key 'message'. Check for that. 