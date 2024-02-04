import express, { Request, Response } from 'express';
import chatRoutes from './routes/chatRoutes'; 
import cors from 'cors';

const app = express();
const port = 3000; 

app.use(cors())
app.use(express.json());

app.use('/api/v1/chat',chatRoutes)

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
