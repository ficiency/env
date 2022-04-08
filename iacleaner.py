
def cleaner(txt):
    import time
    import csv
    import pandas as pd
    import numpy as np

    inite = time.time()
    #print("underwood")
    use_or_non = pd.read_csv("database.csv", encoding='latin-1', on_bad_lines = "skip")[["v1", "v2"]]
    use_or_non.columns = ["label", "text"]
    use_or_non.head()

    use_or_non["label"].value_counts()
    #print("underwood2")
    import string
    punctuation = set(string.punctuation)
    def tokenize(sentence):
        tokens = []
        for token in sentence.split():
            new_token = []
            for character in token:
                if character not in punctuation:
                    new_token.append(character.lower())
            if new_token:
                tokens.append("".join(new_token))
        return tokens

    #print("underwood3")
    use_or_non.head()["text"].apply(tokenize)

    from sklearn.feature_extraction.text import CountVectorizer
    demo_vectorizer = CountVectorizer(
        tokenizer = tokenize,
        binary = True
    )
    #print("underwood4")
    from sklearn.model_selection import train_test_split
    train_text, test_text, train_labels, test_labels = train_test_split(use_or_non["text"], use_or_non["label"], stratify=use_or_non["label"])
    print(f"Training examples: {len(train_text)}, testing examples {len(test_text)}")

    real_vectorizer = CountVectorizer(tokenizer = tokenize, binary=True)
    train_X = real_vectorizer.fit_transform(train_text)
    test_X = real_vectorizer.transform(test_text)
    #print("underwood5")
    from sklearn.svm import LinearSVC
    classifier = LinearSVC()
    classifier.fit(train_X, train_labels)
    LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
            intercept_scaling=1, loss='squared_hinge', max_iter=1000,
            multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
            verbose=0)

    #print("underwood6")
    from sklearn.metrics import accuracy_score
    predicciones = classifier.predict(test_X)
    accuracy = accuracy_score(test_labels, predicciones)
    print(f"Accuracy: {accuracy:.4%}")
    #print("underwood7")
    frases_X = real_vectorizer.transform(txt)
    predicciones = classifier.predict(frases_X)
    #print("underwood8")
    frases_X = real_vectorizer.transform(txt)
    predicciones = classifier.predict(frases_X)
    texts = list()
    nontexts = list()
    #print("underwood9")
    for text, label in zip(txt, predicciones):
        #print(f"{label:5} - {text}")
        if label == "use":
            texts.append(text)
        elif label =="non":
            nontexts.append(text)
    #print("f. underwood")
    end = time.time()
    time_cleaner = end-inite
    print("{:2f} segundos en IAcleaner.py".format(time_cleaner))
    print(nontexts)
    return texts, nontexts, accuracy

