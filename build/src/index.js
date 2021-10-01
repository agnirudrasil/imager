"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.imager = void 0;
const axios_1 = require("axios");
const sharp = require("sharp");
const imager = (req, res) => {
    const pipeline = sharp();
    const url = req.query.url;
    const token = req.query.token;
    if (token !== process.env.API_TOKEN) {
        res.status(401).end();
        return;
    }
    if (!url || typeof url === 'object') {
        res.status(401).end();
        return;
    }
    pipeline.png().pipe(res);
    (0, axios_1.default)({
        url,
        responseType: 'stream',
    }).then(async (response) => await new Promise((resolve, reject) => {
        response.data
            .pipe(pipeline)
            .on('finish', resolve)
            .on('error', (e) => reject(e));
    }));
};
exports.imager = imager;
//# sourceMappingURL=index.js.map