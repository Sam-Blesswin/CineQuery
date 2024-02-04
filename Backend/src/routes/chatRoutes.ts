import express from 'express';
import * as chatController from '../controller/chatController';

const router = express.Router();

router.post('/', chatController.processUserQuery);


export default router;