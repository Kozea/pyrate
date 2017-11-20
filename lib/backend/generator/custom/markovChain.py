import glob  # Used by bulk_train()
import pickle  # Used for (de)serialization of the tree
import random
import re


class MarkovChain:
    """
        Markov algorithm from :
        https://github.com/G3Kappa/Adjustable-Markov-Chains
    """
    def __init__(self):
        self.tree = dict()

    def train(self, text, factor=1):
        '''
        Trains the generator on a block of text.
        '''
        # Split text at every space (including tabs and newlines),
        # and remove empty entries. This keeps punctuation at the
        # end of words containing it. If you do not care about
        # punctuation, include it in the split regex.
        words = filter(lambda s: len(s) > 0, re.split(r'[\s]', text))
        # Casing is not as important as punctuation.
        words = [w.lower() for w in words]
        # "For each pair of words contained within the corpus:"
        for a, b in [(words[i], words[i + 1]) for i in range(len(words) - 1)]:
            # If a branch for "a" doesn't exist, create it.
            if a not in self.tree:
                self.tree[a] = dict()
            # If a leaf "b" hasn't yet grown on branch "a", create it w/
            # a value of "factor". Otherwise, add its value multiplied by
            # "factor" to it.
            self.tree[a][b] = factor if b not in self.tree[a] \
                else self.tree[a][b] + self.tree[a][b] * factor

    def train_on_file(self, filename, encodings=None, verbose=False):
        '''
        Trains the generator on a single file.
        '''
        encodings = encodings if encodings is not None else ['utf-8',
                                                             'ISO-8859-1']
        ret = False
        # If your input files have mismatching encoding, try a few, good ones.
        # If all fails, report back.
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    self.train(f.read())
                if verbose:
                    print('Successfully trained on "{0}". '
                          '[ENCODING: {1}]'.format(filename, encoding))
                ret = True
                break
            except UnicodeDecodeError:
                if verbose:
                    print('Unable to decode "{0}" for training. '
                          '[ENCODING: {1}]'.format(filename, encoding))

        if verbose:
            print()

        return ret

    def bulk_train(self, path, verbose=False):
        '''
        Trains the generator on a single file, or on a list of files, and saves
        the state to disk upon finishing. (Uses glob patterns!)
        Returns the number of files successfully parsed and trained on.
        '''
        i = 0
        for filename in glob.glob(path):
            if self.train_on_file(filename, verbose=verbose):
                i += 1
            elif verbose:
                print('Unable to train on "{0}".'.format(filename))

        if verbose:
            print('Successfully trained on {0} files.'.format(i))

        return i

    def save_training(self, file):
        '''
        Serializes the tree to a file.
        '''
        with open(file, 'wb') as f:
            pickle.dump(self.tree, f)

    def load_training(self, file):
        '''
        Deserializes the tree from a file.
        '''
        with open(file, 'rb') as f:
            self.tree = pickle.load(f)

    def generate(self,
                 start_with=None,
                 max_len=0,
                 rand=lambda x: random.random() * x, verbose=False):
        '''
        Yields a sequence of words until a dead end is found or until a maximum
        length, if specified, is reached.
        '''
        if len(self.tree) == 0:
            return

        # Start with a given word, or randomize one that exists already.
        word = start_with if start_with is not None \
            else random.choice([key for key in self.tree])

        if verbose:
            print('Generating a sentence of {0}, starting with "{1}":\n'
                  .format('max. {0} words'.format(max_len)
                          if max_len > 0
                          else 'unspecified length', word))

        # Yield the starting word
        yield word

        i = 1
        while max_len == 0 or i < max_len:
            i += 1
            # If this word doesn't have a first-level entry in the tree
            # (i.e. no word was ever found next to it during training),
            # stop yielding. We've reached a dead end.
            if word not in self.tree:
                return

            # Otherwise, randomize against the weight of each leaf word divided
            # by the number of leaves.
            dist = sorted([(w, rand(self.tree[word][w] / len(self.tree[word])))
                          for w in self.tree[word]],
                          # And sort the result in decreasing order.
                          key=lambda k: 1-k[1])
            # And yield the highest scoring word
            word = dist[0][0]
            yield word

    def generate_formatted(self,
                           word_wrap=80,
                           soft_wrap=True,
                           newline_chars='.?!',
                           capitalize_chars='.?!"',
                           start_with=None,
                           max_len=0,
                           rand=lambda x: random.random() * x, verbose=False):
        '''
        Same as generate(), but formats the output nicely.
        '''
        # Word-wrap counter
        ww = 0
        # Last character. If capitalization is required, make the first word
        # capitalized.
        lc = capitalize_chars[0] if len(capitalize_chars) > 0 else ''

        for w in self.generate(start_with=start_with,
                               max_len=max_len,
                               rand=rand,
                               verbose=verbose):
            # Capitalize if the last character was a capitalization character,
            # or if the first one is.
            # The latter gotcha might be useful if one wants to capitalize text
            # inside quotation marks, for example.
            wstr = w.capitalize() if lc in capitalize_chars \
                                  else w[0] + w[1:].capitalize() \
                                  if w[0] in capitalize_chars else w
            wstr += ' ' if w[-1] not in newline_chars else '\n'

            if word_wrap > 0:
                ww += len(wstr)
                if wstr[-1] == '\n':
                    ww = 0

                if ww >= word_wrap:
                    # Soft wrap = words can exceed the margin
                    if soft_wrap:
                        wstr += '\n'
                        ww = 0
                    # Hard wrap = words get truncated at the margin
                    else:
                        i = len(wstr) - ww + word_wrap
                        wstr = wstr[:i] + '\n' + wstr[i:]
                        ww -= word_wrap

            yield wstr
            # -2 because the actual last character is either a space or a
            # newline.
            lc = wstr[-2]
