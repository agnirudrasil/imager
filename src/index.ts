import type {HttpFunction} from '@google-cloud/functions-framework/build/src/functions';
import axios from 'axios';
import sharp = require('sharp');

export const imager: HttpFunction = (req, res) => {
  const pipeline = sharp();
  const url = req.query.url;
  if (!url || typeof url === 'object') {
    res.status(401).end();
    return;
  }
  pipeline.png().pipe(res);
  axios({
    url,
    responseType: 'stream',
  }).then(
    async response =>
      await new Promise((resolve, reject) => {
        (response as any).data
          .pipe(pipeline)
          .on('finish', resolve)
          .on('error', (e: Error) => reject(e));
      })
  );
};
