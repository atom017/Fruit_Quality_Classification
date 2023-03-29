import React,{useEffect, useState} from 'react'
import styles from '../../src/style/main.css'
const ImageUpload = () => {
    const api = 'http://127.0.0.1:5000/'
    const [image, setImage] = useState(null);
    const [message,setMessage] = useState(null);
    const [response, setResponse] = useState(null)
    const [preview,setPreview] = useState(null);
    
    const handleImageChange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = () => {
            setImage(file);
            setPreview(reader.result);
        };

        reader.readAsDataURL(file);
    };
  
    const handleFormSubmit = async (event) => {
      event.preventDefault();
  
      const formData = new FormData();
      formData.append('image', image);
  
      const res = await fetch(api+'/upload', {
        method: 'POST',
        body: formData
      });

      setResponse(res)
      
    
    };

    useEffect(() =>{
        if (response) {
            response.json().then(data => {
              if (response.ok) {
                console.log('Image uploaded successfully! ', data.message)
                setMessage(data.message)
              } else {
                console.error('Error uploading image!')
              }
            })
            
          }
    },[response])

    useEffect(() =>{
     setMessage(null)
    },[image])
  
    return (
      <mian className='main'>
        <h1 className='app-title'>Fruit Quality Classification</h1>
        <p className='app-info'>Fruit Types: Apple, Banana, Orange</p>
          <div className='center'>
        
        <form onSubmit={handleFormSubmit} className='form-input'>
        <label htmlFor="image-input" >Choose Image</label>
        <input 
            type="file" 
            id='image-input' 
            accept='image/*'
            onChange={(e) =>handleImageChange(e)}
            />
            <div>
            {preview && (<div>
              <img src={preview} alt="Preview" className='perview' width="200" />
            </div>
            )}
            </div>
           
          <button type="submit" className='submit-btn'>Get Result</button>
        </form>
        <div className='output-container'>
          <span>Output:</span>{message && <h2 className='output'>  {message}</h2>}
        </div>
        
        
      </div>
      
      </mian>
      )
}

export default ImageUpload