// const fs = require('fs')
import fs from 'fs';
import { splitSentences } from './utils.js';

const path = './chameleon_old/chameleon_recsys/data/contentdata/home/lemeiz/content_refine/';


const evaluateText =  (textArray) => {
	let maxWord = 0, sentenceSize = 0;
	if (Array.isArray(textArray)) {
		textArray.forEach(v => { 
			maxWord = Math.max(maxWord, v.split(' ').length)
		});
		// return textArray.forEach((v)=> v.includes('.'));
		sentenceSize = textArray.length;
	}
	return {sentenceAmount: sentenceSize, maxWord: maxWord};

}


const extractText = (json) => {
	const textObj = json.fields.find(field => field.field == 'body');
	if(textObj != undefined) {
		return typeof textObj['value'] == 'object' ? textObj['value'] : [textObj['value']];
	} else {
		return [''];
	}
};

// const files = fs.readdirSync(path);

const acc = [];
const texts = [];

export const retrieveFileContent = (file_path) => {
  const fileContent = fs.readFileSync(file_path);
  return JSON.parse(fileContent);
};

// files.forEach(file => {
// 	const readedFile = fs.readFileSync(`${path}${file}`);
// 	const fileParsed = JSON.parse(readedFile);
// 	texts.push(extractText(fileParsed));
// 	size = evaluateText(extractText(fileParsed));
// 	acc.push(size);
// 	if (size[1] > 1000) {
// 		console.log(fileParsed);
// 		console.log(size);
// 		console.log(fileParsed.fields.find(e => e.field == 'body'));
// 	}
// });

// console.log('starting');
// texts.forEach((textArray => evaluateText(textArray)));
// console.log('finished');
// firsts = acc.sort((a, b) => b[1] - a[1]).slice(0, 50);
// console.log(firsts);
// console.log(texts);

const main = (folder_path) => {
  const files = fs.readdirSync(folder_path);
  const allFilesContent = files.map(file => retrieveFileContent(`${folder_path}/${file}`));
  const extractedTexts = allFilesContent.map(file_object => extractText(file_object));
  const textSentences = extractedTexts.map(textArray => splitSentences(textArray));
  const evaluatedTexts = textSentences.map(text => evaluateText(text));
  const result = evaluatedTexts.sort((a, b) => b.maxWord - a.maxWord).slice(0, 100);
  console.log(result);
}

main('/home/victor/tcc/chameleon_old/chameleon_recsys/data/contentdata/home/lemeiz/content_refine/');
