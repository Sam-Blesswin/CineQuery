import { Request, Response } from 'express';
import axios from 'axios';

export const processUserQuery = async(req: Request,res: Response)=>{
    const message = req.body.message;

    console.log(message);

    const response = await axios.post('http://127.0.0.1:5000/process',{
        message: message
    })

    res.status(200).json(response.data);
}
