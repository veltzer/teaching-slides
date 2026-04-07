import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import { pathToFileURL } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default {
  allowLocalFiles: true,
  baseUrl: pathToFileURL(resolve(__dirname)).href + '/',
};
