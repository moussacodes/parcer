import sys
import platform
import os
from c_token import Token
from c_utils import IS_DELIMITER, IS_KEYWORD, IS_COMPARATOR, IS_OPERATOR
from c_types import TokenType
from ast_logic import init_parse


 
def tokenize(line: str, lineNumber: int):
    tokens: Token = []
    i = 0
    index = 1
    length = len(line)
    
    while i < length:
        if line[i].isspace():
            index += 1
            i += 1
            continue
        
		# check if token is a delimeter
        if IS_DELIMITER(line[i]):
            token = Token(TokenType.TOKEN_DELIMITER, line[i], lineNumber, index-len(line[i]))
            tokens.append(token)
        
        elif IS_COMPARATOR(line[i]):
            temp = line[i]
            index += 1
            
            if i + 1 < length and line[i + 1] == '=':
                temp += '='
                i += 1
                index += 1
            
            token = Token(TokenType.TOKEN_COMPARATOR, temp, lineNumber, index-len(temp))
            tokens.append(token)
			
        
        elif IS_OPERATOR(line[i]):
            temp = line[i]
            op = ""
            index += 1
            temp_type = TokenType.TOKEN_OPERATOR
            if((temp == '+' and line[i+1] == '+') or (temp == '-' and line[i+1] == '-')):
                op += temp + line[i+1]
                i+=2
                token = Token(TokenType.TOKEN_PREASSIGN_INCREMENTER, op, lineNumber, index-len(op))
                tokens.append(token)
                continue
            if(line[i] == '/' and line[i+1] == '/'):
                break
			
            
            if i + 1 < length and line[i + 1] == '=':
                temp += '='
                i += 1
                index += 1
            
            if temp == '->':
                temp_type = TokenType.TOKEN_PTR_CALL
                i += 1
                index += 1
            
            
            token = Token(temp_type, temp, lineNumber, index-len(temp))
            tokens.append(token)
        
        elif line[i].isnumeric():
            num = line[i]
            index += 1
            temp = i + 1
            
			#check if token is number (int, float, ect....)
            while temp < length and (line[temp].isdigit() or line[temp] == '.'):
                num += line[temp]
                temp += 1
                i += 1
                index += 1
            
            token = Token(TokenType.TOKEN_NUMBER, num, lineNumber, index-len(num))
            tokens.append(token)
        
        elif line[i].isalpha() or line[i] == '#':
            word = line[i]
            index += 1
            temp = i + 1
            token_type = TokenType.TOKEN_IDENTIFIER
            if((line[temp] == '+' and line[temp+1] == '+') or (line[temp] == '-' and line[temp+1] == '-')): # detect loop increment, (ex: t++, i--)
                token_type = TokenType.TOKEN_LOOP_OPERATOR
                word += line[temp] + line[temp+1]
                index += 2
                temp += 2
                i += 2
            
            while temp < length and (line[temp].isalpha() or line[temp] == '_'):
                word += line[temp]
                temp += 1
                i += 1
                index += 1
            
            if IS_KEYWORD(word):
                token_type = TokenType.TOKEN_KEYWORD
            
            token = Token(token_type, word, lineNumber, index-len(word))
            tokens.append(token)
        else:
            tokens.append(Token(TokenType.TOKEN_UNKNOWN, line[i], lineNumber, index-len(line[i])))

        i += 1   



    return tokens







def read_file(file_path: str):

    file1 = open(file_path, "r")

    inside_multi_line_comment = False
    lineNumber = 1
    tokens: [Token] = []
    while True:
        line = file1.readline()
        if not line:
            break

    
        if inside_multi_line_comment:
    
            if "*/" in line:
                inside_multi_line_comment = False
    
                line = line.split("*/", 1)[1]
            else:
                lineNumber+=1
                continue  # Skip this line if still inside a comment
        else:
            # Check if the line starts a multi-line comment
            if "/*" in line:
                inside_multi_line_comment = True
                # Remove everything before and including "/*"
                line = line.split("/*", 1)[0]
                

        # Tokenize the line (outside of comments)
        for it in tokenize(line, lineNumber):
            tokens.append(it)
        # for tok in tokens:
        #     print(tok)
        
        lineNumber += 1
    init_parse(tokens)


    file1.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            delemiter = ''
            delimiter = '\\' if platform.system() == "Windows" else '/' 
            source_file = file_path.split(delimiter)[-1]
            if source_file.lower().endswith(".c"):
                read_file(file_path)
            else:
                raise Exception(f"Wrong File Type, {source_file} is not a valid C file")
        else:
            raise Exception(f"File Not Found, {file_path} does not exist")
    else:
        raise Exception("Not Enough Arguments, you should include a valid c file to parse")