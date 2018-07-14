# Natural Language Processing
# Assignment - 1
# Creator : Abhianshu Singla
# NID : ab808557
# Used Atom for writing python Script
# Python version - 3.5.2
# While running, it takes two inputs - the file paths of source file and target file


# import statements
import sys

# Reading the arguments from the terminal and open the source file.
# Returns the source string.
def readInput():
    print("\n\nInput Sentence:")
    input_words = []
    input_tags = []

    source_file = open(str(sys.argv[1]), "r")
    source_string = str(source_file.read())

    sequence = source_string.split("\n")
    for i in range(len(sequence)):
        print(sequence[i], end = " ")
        if(len(sequence[i]) > 0):
            word,tag = sequence[i].split("/")
            input_words.append(word)
            input_tags.append(tag)
        else:
            # Deleting the empty new line character
            del sequence[len(sequence) - 1]

    return sequence, input_words, input_tags


def corpusData():
    # Corpus File path
    # corpus_file = open("/Users/abhianshusingla/Downloads/CAP6640-prog3-distro/wsj-clean.txt")
    corpus_file = open("./wsj-clean.txt")
    #corpus_file = open("/Users/abhianshusingla/Documents/NLP/new_corpus.txt")
    corpus_string = str(corpus_file.read())

    # Data Structures to corpus data
    corpus_dictionary = {}
    token_list = []
    tag_list = []

    # Parameters for counting the relevant data in corpus
    sentence_count = 0
    rightArc_count = 0
    leftArc_count = 0
    root_arc_count = 0

    # Temporary Variables
    temp_list = []

    # Reading the corpus file line by line
    sentences = corpus_string.split("\n")
    for k in range(len(sentences)):

        # Tokenize every word in a sentence
        words = []
        temp_words1 = sentences[k].split("\t")
        for j in range(len(temp_words1)):
            temp_words2 = temp_words1[j].split(" ")
            words.extend(temp_words2)

        # End of Sentence
        if(len(words) < 2):
            # countingArcs(corpus_dictionary, temp_list, root_arc_count, rightArc_count, leftArc_count)
            # Counting the arcs in a sentence
            for i in range(len(temp_list)):
                if(temp_list[i][3] == 0):
                    root_arc_count += 1
                elif(temp_list[i][0] > temp_list[i][3]):
                    rightArc_count += 1
                    tag1 = temp_list[i][2]
                    tag2 = temp_list[temp_list[i][3] - 1][2]
                    key = (tag1, tag2, 'R')
                    if(key in corpus_dictionary):
                        corpus_dictionary[key] += 1
                    else:
                        corpus_dictionary[key] = 1
                elif(temp_list[i][0] < temp_list[i][3]):
                    leftArc_count += 1
                    tag1 = temp_list[i][2]
                    tag2 = temp_list[temp_list[i][3] - 1][2]
                    key = (tag1, tag2, 'L')
                    if(key in corpus_dictionary):
                        corpus_dictionary[key] += 1
                    else:
                        corpus_dictionary[key] = 1

            sentence_count += 1
            temp_list = []

        elif(len(temp_list) != 0 and int(words[0]) == 1):

            # countingArcs(corpus_dictionary, temp_list, root_arc_count, rightArc_count, leftArc_count)
            # Counting the arcs in a sentence
            for i in range(len(temp_list)):
                if(temp_list[i][3] == 0):
                    root_arc_count += 1
                elif(temp_list[i][0] > temp_list[i][3]):
                    rightArc_count += 1
                    tag1 = temp_list[i][2]
                    tag2 = temp_list[temp_list[i][3] - 1][2]
                    key = (tag1, tag2, 'R')
                    if(key in corpus_dictionary):
                        corpus_dictionary[key] += 1
                    else:
                        corpus_dictionary[key] = 1
                elif(temp_list[i][0] < temp_list[i][3]):
                    leftArc_count += 1
                    tag1 = temp_list[i][2]
                    tag2 = temp_list[temp_list[i][3] - 1][2]
                    key = (tag1, tag2, 'L')
                    if(key in corpus_dictionary):
                        corpus_dictionary[key] += 1
                    else:
                        corpus_dictionary[key] = 1


            sentence_count += 1
            temp_list = []

            token_list.append(words[1])
            tag_list.append(words[2])
            words[0] = int(words[0])
            words[3] = int(words[3])

            temp_list.append(words)

        else:
            # Continuation of a sentence
            token_list.append(words[1])
            tag_list.append(words[2])
            words[0] = int(words[0])
            words[3] = int(words[3])

            temp_list.append(words)




    tag_list = list(set(tag_list))
    tag_list.sort()

    # Printing corpus data
    print("\nCorpus Statistics:\n")
    print("     # sentences  :  ", sentence_count)
    print("     # tokens     : ", len(token_list))
    print("     # POS tags   :    ", len(tag_list))
    print("     # Left-Arcs  : ", leftArc_count)
    print("     # Right-Arcs : ", rightArc_count)
    print("     # Root-Arcs  :  ", root_arc_count)

    return corpus_dictionary, tag_list



def printArcs(corpus_dictionary, tag_list):
    print("\n\nLeft Arc Array Nonzero Counts:")
    for i in range(len(tag_list)):
        print('\n{: <4}'.format(tag_list[i]), " : ", end = "")
        for j in range(len(tag_list)):
            key = (tag_list[i], tag_list[j], 'L')
            if(key in corpus_dictionary):
                #print("[", '{: <4}'.format(tag_list[j]), ",", '{: <4}'.format(corpus_dictionary[key]), "]", end = " ")
                print("[", tag_list[j], ",", corpus_dictionary[key], "]", end = " ")

    print("\n\n\nRight Arc Array Nonzero Counts:")
    for i in range(len(tag_list)):
        print('\n{: <4}'.format(tag_list[i]), " : ", end = "")
        for j in range(len(tag_list)):
            key = (tag_list[i], tag_list[j], 'R')
            if(key in corpus_dictionary):
                #print("[", '{: <4}'.format(tag_list[j]), ",", '{: <4}'.format(corpus_dictionary[key]), "]", end = " ")
                print("[", tag_list[j], ",", corpus_dictionary[key], "]", end = " ")

    print("\n\n\nArc Confusion Array:")
    confusion_arc_count = 0
    for i in range(len(tag_list)):
        print('\n{: <4}'.format(tag_list[i]), " : ", end = "")
        for j in range(len(tag_list)):
            key1 = (tag_list[i], tag_list[j], 'L')
            key2 = (tag_list[i], tag_list[j], 'R')
            if(key1 in corpus_dictionary and key2 in corpus_dictionary):
                #print("[", '{: <4}'.format(tag_list[j]), ",", '{: <4}'.format(corpus_dictionary[key]), "]", end = " ")
                print("[", tag_list[j], ",", corpus_dictionary[key1], ",", corpus_dictionary[key2], "]", end = " ")
                confusion_arc_count += 1
    print("\n\n      Number of confusing arcs = ", confusion_arc_count)


# The oracle performs two functions.
# 1. It determines whether a particular transition is permitted for two given words.
# 2. When multiple transitions are permitted for two given words,
#    it determines which of all possible transitions should be taken by the parser.
def oracle(corpus_dictionary, tag1, tag2, size_stack, size_buffer):

    if(size_buffer == 0 and size_stack == 1):
        print('No Action')

    # Empty stack or 1 element stack without considering root
    if(tag1 == '' or tag2 == ''):
        return 'SHIFT'

    # Special Oracle Rules

    if(tag1[0] == 'V' and (tag2[0] == '.' or tag2[0] == 'R')):
        # Rule 1 - If the first character of the tag for the i-th element is "V" (tag1) and
        # the first character of the tag for the j-th element (tag2) is either "." or "R",
        # then your oracle should return "Right-Arc" as the action for the parser to take
        return 'Right-Arc'
    elif(size_stack > 2 and (tag1[0] == 'I' and tag2[0] == '.')):
        # Rule 2 - If the current size of the stack is greater than two (not including the ROOT node) and
        # the first character of the tag of the i-th element (tag1) is either "I" and tag2 starts with ".",
        # then the oracle should return "SWAP" for the parser action
        return 'SWAP'
    elif(size_buffer != 0 and (tag1[0] == 'V' or tag1[0] == 'I')):
        # Rule 3 - If the buffer is non-empty and
        # the first character of the tag for the i-th element (tag1) is either "V" or "I" and
        # the first character of the tag for the j-th element (tag2) is either "D", "I", "J", "P", or "R",
        # then the oracle should return "SHIFT" for the parser action.
        if(tag2[0] == 'D' or tag2[0] == 'I' or tag2[0] == 'J' or tag2[0] == 'P' or tag2[0] == 'R'):
            return 'SHIFT'

    key1 = (tag1, tag2, 'L')
    key2 = (tag1, tag2, 'R')
    if(key1 in corpus_dictionary and key2 in corpus_dictionary):
        # Confusion Arcs
        if(corpus_dictionary[key1] > corpus_dictionary[key2]):
            return 'Left-Arc'
        else:
            return 'Right-Arc'
    elif(key1 in corpus_dictionary):
        return 'Left-Arc'
    elif(key2 in corpus_dictionary):
        return 'Right-Arc'
    else:
        return 'SHIFT'


# Printing the stack_
def printStack(stack_):
    print("[", end = "")
    for i in range(len(stack_)):
        if(i > 0):
            print(",", end = "")
        print(stack_[i], end = "")
    print("]", end = "")


#Printing the buffer_
def printBuffer(buffer_):
    print("[", end = "")
    for i in range(len(buffer_)):
        if(i > 0):
            print(",", end = "")
        print(buffer_[i], end = "")
    print("]", end = "")



# Transition-based Dependency Parser
def parser(sequence, input_words,input_tags,corpus_dictionary):

    # Using list as a stack
    stack_ = []

    # Using list as a buffer
    buffer_ = sequence[:]
    i = 1

    while(True):
        size_stack = len(stack_)
        size_buffer = len(buffer_)
        tag1 = ''
        tag2 = ''
        val1 = ''
        val2 = ''

        if(size_buffer == 0 and size_stack == 1):
            printStack(stack_)
            printBuffer(buffer_)
            print("ROOT", "-->", stack_.pop())
            break;


        printStack(stack_)
        printBuffer(buffer_)

        if(size_stack >= 2):
            val2 = stack_.pop()
            val1 = stack_.pop()
            tag2 = val2.split('/')[1]
            tag1 = val1.split('/')[1]

        action = oracle(corpus_dictionary, tag1, tag2, size_stack, size_buffer)
        if(action == 'SHIFT'):
            print("SHIFT")
            if(val1 != '' and val2 != ''):
                stack_.append(val1)
                stack_.append(val2)
            if(len(buffer_) != 0):
                stack_.append(buffer_[0])
                del buffer_[0]
            else:
                print("This parser doesn't support all sentences and ending the program here.")
                break;
        elif(action == 'SWAP'):
            buffer_.insert(0,val1)
            stack_.append(val2)
            print("SWAP")
        elif(action == 'Left-Arc'):
            print("Left-Arc:", val1, "<--", val2)
            stack_.append(val2)
        elif(action == 'Right-Arc'):
            print("Right-Arc:", val1, "-->", val2)
            stack_.append(val1)




# Printing header of the program output
print("")
print("University of Central Florida")
print("CAP6640 Spring 2018 - Dr. Glinos")
print("Dependency Parser by Abhianshu Singla")

corpus_dictionary, tag_list = corpusData()
printArcs(corpus_dictionary, tag_list)
sequence, input_words, input_tags = readInput()

print("\n\n\nParsing Actions and Transitions:\n")
parser(sequence, input_words,input_tags,corpus_dictionary)
