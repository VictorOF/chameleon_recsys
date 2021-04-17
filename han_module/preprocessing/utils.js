// expects to receive an array of strings and return a list of sentences.
// we can't guarantee that there are two sentences in a received string, so I have to split each one
export const splitSentences = (textArray) => {
  return textArray.map((text) => {
    return text.split(".").map(string => string.trim());
  }).flat();
};
