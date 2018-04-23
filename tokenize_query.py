# Tokenize query
# Eg. "swimming pool" and teacher

def tokenize_query(query_string):
  query_string.strip(' ')
  index = 0
  query_phrases = []
  while True:
    if index >= len(query_string):
      break
    
    character = query_string[index]

    if character == '"':
      index += 1
      query_phrase = ""
      while True:
        character = query_string[index]
        if character == '"':
          query_phrases.append(query_phrase)
          index += 1
          break
        query_phrase += character
        index += 1

    if index == 0:
      character = ' '
      index = -1

    if character == ' ':
      index += 1
      query_phrase = ""
      while True:
        if index >= len(query_string):
          query_phrases.append(query_phrase)
          break

        character = query_string[index]
        
        if character == '"':
          break

        if character == ' ':
          query_phrases.append(query_phrase)
          break
        query_phrase += character
        index += 1

  return query_phrases
      
if __name__ == "__main__":
  phrases = tokenize_query('"something like" and hi')
  assert phrases == ['something like', 'and', 'hi'], phrases

  phrases = tokenize_query('"something like" and "hi"')
  assert phrases == ['something like', 'and', 'hi'], phrases

  phrases = tokenize_query('"hi"')
  assert phrases == ['hi'], phrases

  phrases = tokenize_query('"hi" and "hi2"')
  assert phrases == ['hi', 'and', 'hi2'], phrases
  
  phrases = tokenize_query('quiet phone call')
  assert phrases == ['quiet', 'phone', 'call'], phrases