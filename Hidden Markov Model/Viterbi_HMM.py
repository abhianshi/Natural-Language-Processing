# Natural Language Processing
# Assignment - 2
# Creator : Abhianshu Singla
# NID : ab808557
# Used Atom for writing python Script
# Python version - 3.5.2
# While running, it takes two inputs - the file paths of source file and target file


# import statements
import sys

def print_header():
    # Printing header of the program output
    print("")
    print("University of Central Florida")
    print("CAP6640 Spring 2018 - Dr. Glinos\n")
    print("Viterbi Algorithm HMM Tagger by Abhianshu Singla\n\n")


# Reading the arguments from the terminal and identifying the source file and target file.
# Returns the source string and target string.
def read():
    training_corpus = open(str(sys.argv[1]), "r")
    test_file = open(str(sys.argv[2]), "r")
    train_string = str(training_corpus.read())
    test_string = str(test_file.read())
    return train_string, test_string


# converting the tokens into lower case
def lower_case(tokens_list):
    length = len(tokens_list)
    for i in range(length):
        tokens_list[i] = tokens_list[i].lower()
    return tokens_list


# Tokenizing the training data
def tokenization_train(train_string):
    line_split = train_string.split("\n")
    tokens = []
    tagsets = []
    sentence_start = []
    count = 0
    sentence_start.append(0)
    for i in range(len(line_split)):
        word_split = line_split[i].split(" ")
        if len(word_split) != 1 :
            tokens.append(word_split[0])
            tagsets.append(word_split[1])
        else:
            sentence_start.append(i-count)
            count += 1
    return sentence_start,tokens,tagsets

# Tokenizing the test data
def tokenization_test(test_string):
    line_split = test_string.split("\n")
    test_tokens = []
    sentence_start_test = []
    for i in range(len(line_split)):
        sentence_start_test.append(len(test_tokens))
        test_tokens.extend(line_split[i].split(" "))
    return test_tokens, sentence_start_test


# If the lower case word ends with "sses" or "xes", then drop the last 2 characters;
# Else if it ends with "ses" or "zes", then drop only the last character;
# Else if it ends with"ches" or "shes", then drop the last 2 characters;
# Else if it ends with "men", then change the last 2 characters to "an";
# Else if it ends with "ies", then drop the last 3 characters and add "y".
# Lemmatizing the input
def lemmatization(tokens_list):
    for i in range(len(tokens_list)):
        if(tokens_list[i].endswith("sses") | tokens_list[i].endswith("xes")):
            tokens_list[i] = tokens_list[i][:-2]
        elif(tokens_list[i].endswith("ses") | tokens_list[i].endswith("zes")):
            tokens_list[i] = tokens_list[i][:-1]
        elif(tokens_list[i].endswith("ches") | tokens_list[i].endswith("shes")):
            tokens_list[i] = tokens_list[i][:-2]
        elif(tokens_list[i].endswith("men")):
            tokens_list[i] = tokens_list[i][:-2] + "an"
        elif(tokens_list[i].endswith("ies")):
            tokens_list[i] = tokens_list[i][:-3] + "y"

    return tokens_list

# All the unique tags in the corpus data
def all_tags(tagsets):
    # Unique Tagsets by converting the tagsets list into set
    set_tags = list(set(tagsets))
    set_tags.sort()
    tag_count = len(set_tags)
    print("All Tags Observed:\n")
    for i in range(tag_count):
        print('{: <3}{}'.format(i+1,set_tags[i]))

    return set_tags


# Initial Distribution of the corpus data
def initial_distribution(sentence_count,sentence_start,set_tags):
    print("\nInitial Distribution:\n")
    start_tags = []
    initial_dist = []
    temp = 0
    for i in range(sentence_count):
        start_tags.append(tagsets[sentence_start[i]])
    for i in range(len(set_tags)):
        initial_dist.append([set_tags[i],round((start_tags.count(set_tags[i])/sentence_count),6),start_tags.count(set_tags[i])])
        if(initial_dist[i][1] != 0.0):
            print("start [",initial_dist[i][0],"|  ]",initial_dist[i][1])
            temp += initial_dist[i][2]

    return initial_dist

# Emission Probabilities of the tags
def emission_probability(set_tags,tokens,tagsets):
    print("\nEmission Probabilities:\n")

    # Counting the occurences of each tag in the corpus
    tags_count = {}
    for i in range(len(set_tags)):
        tags_count[set_tags[i]] = tagsets.count(set_tags[i])

    # Counting the occurences of each token in the corpus
    token_tags = {}
    for i in range(len(tokens)):
        if((tokens[i],tagsets[i]) in token_tags):
            token_tags[(tokens[i],tagsets[i])] = token_tags[(tokens[i],tagsets[i])] + 1
        else:
            token_tags[(tokens[i],tagsets[i])] = 1

    # After sorting a dictionary becomes a list in python
    sorted_token_tags = sorted(token_tags)
    emission_prob = []

    for i in range(len(sorted_token_tags)):
        emission_prob.append((sorted_token_tags[i][0],sorted_token_tags[i][1],round(token_tags[sorted_token_tags[i]]/tags_count[sorted_token_tags[i][1]],6)))
        print('{: <25}{: <5}{:f}'.format(emission_prob[i][0],emission_prob[i][1],emission_prob[i][2]))

    return tags_count,emission_prob


# Transition probabilities of bigrams
def transition_probability(initial_dist,tags_count,sentence_start,set_tags,tokens,tagsets):
    transition_prob = {}
    print("\nTransition Probabilities:\n")

    # Printing initial distribution again in transition probabilities
    temp = 0
    for i in range(len(initial_dist)):
        temp += initial_dist[i][1]
    print("[",temp,"]   ", end = "")
    for i in range(len(initial_dist)):
        if(initial_dist[i][1] != 0.0):
            #transition_prob.append((" ",initial_dist[i][0],initial_dist[i][1]))
            transition_prob[(" ",initial_dist[i][0])] = initial_dist[i][1]
            print("[",initial_dist[i][0],"| ]",initial_dist[i][1], end = "   ")
    print()

    tags_tags = {}
    j = 1
    for i in range(len(tokens) - 1):
        if( i + 1 != sentence_start[j]):
            if((tagsets[i],tagsets[i+1]) in tags_tags):
                tags_tags[(tagsets[i],tagsets[i+1])] = tags_tags[(tagsets[i],tagsets[i+1])] + 1
            else:
                tags_tags[(tagsets[i],tagsets[i+1])] = 1
        else:
            if((tagsets[i]," ") in tags_tags):
                tags_tags[(tagsets[i]," ")] = tags_tags[(tagsets[i]," ")] + 1
            else:
                tags_tags[(tagsets[i]," ")] = 1
            j += 1

    # After sorting a dictionary becomes a list in python
    sorted_tags_tags = sorted(tags_tags)

    i = 0
    while(i < len(sorted_tags_tags)):
        print("[ 1.000000 ]   ", end = "")
        characters = sorted_tags_tags[i][0]
        while(i < len(sorted_tags_tags) and characters == sorted_tags_tags[i][0]):
            transition_prob[(sorted_tags_tags[i][0],sorted_tags_tags[i][1])] = round(tags_tags[sorted_tags_tags[i]]/tags_count[sorted_tags_tags[i][0]],6)
            print("[",sorted_tags_tags[i][1],"|",sorted_tags_tags[i][0],"]",'{:f}'.format(tags_tags[sorted_tags_tags[i]]/tags_count[sorted_tags_tags[i][0]]), end = " ")
            i += 1
        print()

    return transition_prob


# Corpus Features
def corpus_features(tags,bigrams,lexicals,sentences):
    print("\nCorpus Features:\n")
    print("Total # tags        :",tags)
    print("Total # bigrams     :",bigrams)
    print("Total # lexicals    :",lexicals)
    print("Total # sentences   :",sentences)


 # Initial probability of test tokens
def initial_probability_test(initial_test_tokens,test_tokens,emission_prob):
    print("\n\nTest Set Tokens Found in Corpus:\n")
    a,b,c = zip(*emission_prob)
    initial_test = []
    for i in range(len(test_tokens)):
        print('{:<25}'.format(initial_test_tokens[i]), ":  ",end = " ")
        if(test_tokens[i] in a):
            indices = [j for j, x in enumerate(a) if x == test_tokens[i]]
            temp = []
            for j in range(len(indices)):
                print(b[indices[j]],"(",'{:f}'.format(c[indices[j]]),")", end = " ")
                temp.append((b[indices[j]],c[indices[j]]))
            initial_test.append(temp)
        else:
            # If a unigram doesn't exist in the word pool, take it as NN and probability 0.000100
            print("NN (0.000100)", end = "")
            initial_test.append(([("NN",0.000100)]))
        print()
    return initial_test


# Normalization of values
def normalize(temp):
    summation = sum(temp)
    for i in range(len(temp)):
        temp[i] = temp[i]/summation
    return temp


# Imtermediate Probabilities
def intermediate_probability(initial_test_tokens,test_tokens,initial_test,sentence_start_test):
    print("\n\nIntermediate Results of Viterbi Algorithm:")

    intermediate_test = []
    sentence_index = 0
    for i in range(len(test_tokens)):
        temp_val = []
        temp_key = []

        for j in range(len(initial_test[i])):

            if(sentence_index < len(sentence_start_test) and i == sentence_start_test[sentence_index]):
                a = initial_test[i][j][1]
                b = transition_prob[(" ",initial_test[i][j][0])]
                result = a * b
                temp_val.append(result)
                temp_key.append("null")
            else:
                max_val = 0
                max_key = ""
                for k in range(len(initial_test[i-1])):
                    a = intermediate_test[i-1][1][k]
                    b = initial_test[i][j][1]
                    # If a bigram doesn't exist in the word pool, then take its probability to be 0.0001
                    c = 0.0001
                    if((initial_test[i-1][k][0],initial_test[i][j][0]) in transition_prob):
                        c = transition_prob[(initial_test[i-1][k][0],initial_test[i][j][0])]
                    result = a * b * c
                    print("test:",intermediate_test[i-1][0][k],a,b,c)
                    if(result >= max_val):
                        max_val = result
                        max_key = initial_test[i-1][k][0]

                temp_val.append(max_val)
                temp_key.append(max_key)

        if(sentence_index < len(sentence_start_test) and i == sentence_start_test[sentence_index]):
            sentence_index += 1
        temp_val = normalize(temp_val)
        intermediate_test.append((temp_key,temp_val))


    for i in range(len(test_tokens)):
        print("\nIteration  ",i+1,":",'{:<25}'.format(initial_test_tokens[i]),": ",end = "")
        for j in range(len(initial_test[i])):
            p_key = initial_test[i][j][0]
            sec_key = intermediate_test[i][0][j]
            value = intermediate_test[i][1][j]
            print(p_key,"(",'{:f}'.format(value),",", sec_key ,")", end = " ")


    return intermediate_test


# Final Viterbi output
def final_viterbi_output(initial_test_tokens,test_tokens,intermediate_test,initial_test,sentence_start_test):
    print("\n\n\nViterbi Tagger Output:\n")
    final_output = {}
    sentence_index = len(test_tokens) - 1
    k = len(sentence_start_test) - 1
    p_key = ""
    sec_key = ""
    max_val = 0

    for i in range(len(test_tokens)-1,-1,-1):
        if(i == sentence_index):
            p_key = ""
            sec_key = ""
            max_val = 0
            for j in range(len(intermediate_test[i][1])):
                if(intermediate_test[i][1][j] > max_val):
                    max_val = intermediate_test[i][1][j]
                    p_key = initial_test[i][j][0]
                    sec_key = intermediate_test[i][0][j]
            sentence_index = sentence_start_test[k] - 1
            k -= 1
            final_output[initial_test_tokens[i]] = p_key
        else:
            p_key = sec_key
            for j in range(len(initial_test[i])):
                if(p_key == initial_test[i][j][0]):
                    sec_key = intermediate_test[i][0][j]
                    break
            final_output[initial_test_tokens[i]] = p_key

    for i in range(len(test_tokens)):
        print('{:<25}'.format(initial_test_tokens[i]),final_output[initial_test_tokens[i]])

    return final_output



# Start of code
print_header()

# Reading the file names from the terminal
train_string, test_string = read()

# Tokenizing the words and tagsets
sentence_start,tokens,tagsets = tokenization_train(train_string)

# Converting to lower case
tokens = lower_case(tokens)

# lemmatization
tokens = lemmatization(tokens)

# Counting the sentences in the corpus
sentence_count = train_string.count('\n\n')

# Unique Tags in the Corpus
set_tags = all_tags(tagsets)

# Unique words in the corpus
set_tokens = list(set(tokens))

# Initial Distribution
initial_dist = initial_distribution(sentence_count,sentence_start,set_tags)

# Emission Probabilities
tags_count,emission_prob = emission_probability(set_tags,tokens,tagsets)

# Transition Probability
transition_prob = transition_probability(initial_dist,tags_count,sentence_start,set_tags,tokens,tagsets)

# Corpus features
corpus_features(len(set_tags),len(transition_prob),len(set_tokens),sentence_count)

# Test files and Test Tokenization
initial_test_tokens, sentence_start_test = tokenization_test(test_string)
test_tokens = lower_case(initial_test_tokens[:])
test_tokens = lemmatization(test_tokens)

# Initial probabilities of test tokens
initial_test = initial_probability_test(initial_test_tokens,test_tokens,emission_prob)

# Intermediate probabilities of test tokens
intermediate_test = intermediate_probability(initial_test_tokens,test_tokens,initial_test,sentence_start_test)

# Final Viterbi Output
final_output = final_viterbi_output(initial_test_tokens,test_tokens,intermediate_test, initial_test,sentence_start_test)
