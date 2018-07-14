# Natural Language Processing
# Assignment - 1
# Creator : Abhianshu Singla
# NID : ab808557
# Used Atom for writing python Script
# Python version - 3.5.2
# While running, it takes two inputs - the file paths of source file and target file


# import statements
import sys

# Reading the arguments from the terminal and identifying the source file and target file.
# Returns the source string and target string.
def read():
    first_file = open(str(sys.argv[1]), "r")
    second_file = open(str(sys.argv[2]), "r")
    len1 = len(first_file.name)

    if(first_file.name[len1 - 7: ] == "src.txt"):
        source_file = first_file
        target_file = second_file
    else:
        source_file = second_file
        target_file = first_file

    print("Source file:",source_file.name.split('/')[-1])
    print("Target file:",target_file.name.split('/')[-1])

    source_string = str(source_file.read())
    target_string = str(target_file.read())

    return source_string, target_string


# Tokenize the source string and target string with whitespace characters
def tokenize(source_string, target_string):
    source_tokens = source_string.split()
    target_tokens = target_string.split()
    return source_tokens, target_tokens


# Normalization 1st step : converting the tokens to lower cases
def lower_case(tokens_list):
    length = len(tokens_list)
    for i in range(length):
        tokens_list[i] = tokens_list[i].lower()
    return tokens_list


# Checks if the character is alphanumeric or not.
def isAlphaNumeric(character):
    # Checking only lowercase letters because in first step of normalization, we are converting all the uppercase letters to lowercase letters
    if((character >= 'a' and character <= 'z') or (character >= '0' and character <= '9')):
        return True
    else:
        return False


# Checks if the word is a special word with special characters or not.
def isSpecialCase(word):
    for i in range(len(word)):
        if(isAlphaNumeric(word[i])):
            return False

    return True


# Normalization 2nd step : splitting the initial special characters.
def start_alphanumeric_normalize(tokens_list):
    length = len(tokens_list)
    shift = 0

    for i in range(length):
        j = 0
        index = i + shift
        word = tokens_list[index]

        if(not isSpecialCase(word) and not isAlphaNumeric(word[j])):

            while(j < len(word) and not isAlphaNumeric(word[j]) ):
                tokens_list.insert(index + j, str(word[j]))
                j += 1
                shift += 1

            if(j != len(word)):
                tokens_list[i + shift] = word[j:]

    return tokens_list


# Normalization 3rd step : splitting the initial special characters.
def trail_alphanumeric_normalize(tokens_list):
    length = len(tokens_list)
    shift = 0

    for i in range(length):
        index = i + shift
        word = tokens_list[index]
        j = len(word) - 1

        if(not isSpecialCase(word) and not isAlphaNumeric(word[j])):

            while(j > 0 and not isAlphaNumeric(word[j]) ):
                tokens_list.insert(index + 1, str(word[j]))
                j -= 1
                shift += 1

            if(j != 0):
                tokens_list[index] = word[:j+1]

    return tokens_list


# Normalization 4th step : replacing the apostrophe with full words.
def apostrophe_normalize(tokens_list):
    length = len(tokens_list)
    shift = 0

    for i in range(length):

        index = i + shift
        word = tokens_list[index]
        j = len(word)

        if(j >= 3 and word[j-2:] == "'s"):
            tokens_list[index] = str(word[ :j-2])
            tokens_list.insert(index + 1, "'s")
            shift += 1

        elif(j >= 4 and word[j-3:] == "n't"):
            tokens_list[index] = str(word[ :j-3])
            tokens_list.insert(index + 1, "not")
            shift += 1

        elif(j >= 3 and word[j-2:] == "'m"):
            tokens_list[index] = str(word[ :j-2])
            tokens_list.insert(index + 1, "am")
            shift += 1

    return tokens_list


# Normalization
def normalize(source_tokens, target_tokens):

    # Rule 1. Convert tokens to lower case
    source_tokens = lower_case(source_tokens)
    target_tokens = lower_case(target_tokens)

    # Rule 2. Separating starting non-alphanumeric character
    source_tokens = start_alphanumeric_normalize(source_tokens)
    target_tokens = start_alphanumeric_normalize(target_tokens)

    # Rule 4. Sub rules with apostrophe
    source_tokens = apostrophe_normalize(source_tokens)
    target_tokens = apostrophe_normalize(target_tokens)

    # Rule 3. Separating trailing non-alphanumeric character
    source_tokens = trail_alphanumeric_normalize(source_tokens)
    target_tokens = trail_alphanumeric_normalize(target_tokens)

    return source_tokens, target_tokens


# Smith Waterman Edit Table and Backtrace Table
def SmithWaterman(source_tokens, target_tokens):

    # Initialization
    editDistance = []
    backtraceTable = []
    for i in range (len(source_tokens) + 1):
        dist_row = []
        back_row = []
        for j in range (len(target_tokens) + 1):
            dist_row.append(0)
            back_row.append("")
        editDistance.append(dist_row)
        backtraceTable.append(back_row)

    gap = -1
    match = -1
    for i in range (1,len(source_tokens) + 1):
        for j in range (1,len(target_tokens) + 1):
            match = -1
            if(source_tokens[i-1] == target_tokens[j-1]):
                match = 2
            editDistance[i][j] = max(0, editDistance[i-1][j] + gap, editDistance[i][j-1] + gap, editDistance[i-1][j-1] + match)

            if(editDistance[i][j] != 0):
                if(editDistance[i][j] == editDistance[i-1][j] + gap):
                    backtraceTable[i][j] = "UP"
                elif(editDistance[i][j] == editDistance[i][j-1] + gap):
                    backtraceTable[i][j] = "LT"
                elif(editDistance[i][j] == editDistance[i-1][j-1] + match):
                    backtraceTable[i][j] = "DI"

    return editDistance, backtraceTable


# Calculating the maximum value and all the maximas
def alignment(editDistance):
    maximum_value = 0
    for i in range (len(editDistance)):
        for j in range (len(editDistance[i])):
            if(maximum_value < editDistance[i][j]):
                maximum_value = editDistance[i][j]

    maximas = []
    for i in range (len(editDistance)):
        for j in range (len(editDistance[i])):
            if(maximum_value == editDistance[i][j]):
                maximas.append([i,j])

    return maximum_value, maximas


# Calculating the alignments
def alignments(maximas, backtraceTable, source_tokens, target_tokens):
    print("Maximal-similarity alignments:")
    for i in range(len(maximas)):
        length = 0
        index_i = maximas[i][0]
        index_j = maximas[i][1]
        aligned_source = []
        aligned_target = []
        aligned_action = []
        while(index_i >= 0 and index_j != 0 and backtraceTable[index_i][index_j] != ""):
            length += 1
            if(backtraceTable[index_i][index_j] == "DI"):
                index_i -= 1
                index_j -= 1
                aligned_source.append(source_tokens[index_i])
                aligned_target.append(target_tokens[index_j])
                if(source_tokens[index_i] == target_tokens[index_j]):
                    aligned_action.append("")
                else:
                    aligned_action.append("s")
            elif(backtraceTable[index_i][index_j] == "LT"):
                index_j -= 1
                aligned_source.append("-")
                aligned_target.append(target_tokens[index_j])
                aligned_action.append("i")
            elif(backtraceTable[index_i][index_j] == "UP"):
                index_i -= 1
                aligned_source.append(source_tokens[index_i])
                aligned_target.append("-")
                aligned_action.append("d")

        aligned_action = aligned_action[::-1]
        aligned_target = aligned_target[::-1]
        aligned_source = aligned_source[::-1]

        # For Printing Purposes
        for j in range(len(aligned_source)):
            src_len = len(aligned_source[j])
            tgt_len = len(aligned_target[j])
            if(src_len > tgt_len):
                aligned_target[j] = aligned_target[j].rjust(src_len)
                aligned_action[j] = aligned_action[j].rjust(src_len)
            else:
                aligned_source[j] = aligned_source[j].rjust(tgt_len)
                aligned_action[j] = aligned_action[j].rjust(tgt_len)

        print("\n   Alignment",i,"(length",length,"):")
        print("      Source at   ",index_i,":  ",end = "")
        print(*aligned_source)
        print("      Target at   ",index_j,":  ",end = "")
        print(*aligned_target)
        print("      Edit action    :  ",end = "")
        print(*aligned_action)
        print()

# Printing header of the program output
print("")
print("University of Central Florida")
print("CAP6640 Spring 2018 - Dr. Glinos\n")
print("Text Similarity Analysis by Abhianshu Singla\n")

source_string, target_string = read()
source_tokens, target_tokens = tokenize(source_string, target_string)
print("\nRaw Tokens:")
print("     Source > ", end = "")
print(' '.join(str(p) for p in source_tokens))
print("     Target > ", end = "")
print(' '.join(str(p) for p in target_tokens))

source_tokens, target_tokens = normalize(source_tokens, target_tokens)
print("\nNormalized Tokens:")
print("     Source > ", end = "")
print(' '.join(str(p) for p in source_tokens))
print("     Target > ", end = "")
print(' '.join(str(p) for p in target_tokens))

# Printing tables
target_3 = []
target_3.append("#")
for i in range(len(target_tokens)):
    target_3.append(target_tokens[i][:3])

source_3 = []
source_3.append("#")
for i in range(len(source_tokens)):
    source_3.append(source_tokens[i][:3])

idx_source = [idx[0] for idx in enumerate(source_3)]
idx_target = [idx[0] for idx in enumerate(target_3)]

src = []
for i in range(len(source_3)):
    src.append([i,source_3[i]])
row_format ="{:>5}" * (len(idx_target) + 2)

editDistance, backtraceTable = SmithWaterman(source_tokens, target_tokens)

print("\nEdit Distance Table:\n")
print(row_format.format("","", *idx_target))
print(row_format.format("","", *target_3))
for team, row in zip(src, editDistance):
    print(row_format.format(*team, *row))

print("\nBacktrace Table:\n")
print(row_format.format("","", *idx_target))
print(row_format.format("","", *target_3))
for team, row in zip(src, backtraceTable):
    print(row_format.format(*team, *row))

maximum_value, maximas = alignment(editDistance)
print("\nMaximum value in distance table:",maximum_value)
print("\nMaxima:")
for i in range(len(maximas)):
    print("     ",maximas[i],"\n")

alignments(maximas, backtraceTable, source_tokens, target_tokens)
