import { Request, Response } from 'express';
import axios from 'axios';

interface ErrorResponse {
    response: {
        data: {
            error: string;
        };
    };
}

export const processUserQuery = async(req: Request,res: Response)=>{

    try{
        const message = req.body.message;

        console.log(message);
    
        const response = await axios.post('http://127.0.0.1:5000/process',{
            query: message
        })
    
        console.log(response.data['data'])
    
        res.status(200).json({"outputMessage" : response.data['data']});
    }catch(err: unknown){
        console.log(err);

        if (err instanceof Error && 'response' in err) {
            const errorResponse = err as ErrorResponse;
            res.status(500).json({ "error": errorResponse.response.data['error'] });
        } else {
            res.status(500).json({ "error": "Something went wrong. Please try again later." });
        }
    }
}
