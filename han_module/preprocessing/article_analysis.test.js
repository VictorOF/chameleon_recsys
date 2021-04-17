import { splitSentences } from "./utils.js";


describe("splitSentences return as expect", () => {
  it("return empty array for empty input", () => {
    const textInput = [];
    expect(splitSentences(textInput)).toStrictEqual([]);
  });

  it("return original input if no split is needed", () => {
    const textInput = ["sentence 1", "sentence 2", "sentence 3"]; 
    expect(splitSentences(textInput)).toStrictEqual(textInput);
  });
  it("split all texts", () => {
    const textInput = ["sentence 1. sentence 2", "sentence 3"];
    const expectedOutput = ["sentence 1", "sentence 2", "sentence 3"];
    expect(splitSentences(textInput)).toStrictEqual(expectedOutput);
  });
});
