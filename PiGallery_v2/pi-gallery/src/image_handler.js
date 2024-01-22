import React, { useEffect, useState } from "react";
import img1 from './imgs/1.PNG'
import img2 from './imgs/2.PNG'
import img3 from './imgs/3.png'

const images = [img1, img2, img3]

export default function ImageSwapper() {
    const [currentImage, setCurrentImage] = useState(null);

    useEffect(() => {
        const intervalId = setInterval(() => {
            setCurrentImage(images[Math.floor(Math.random() * images.length)]);
        }, 5000)
        
        return () => clearInterval(intervalId);
    }, [])

    var ratio;
    var resized_height;
    var resized_width;
    const divisor = 2.5

    var wh = window.innerHeight
    var ww = window.innerWidth

    var img = new Image();
    img.src = currentImage;

    if (img.width > img.height) {
        ratio = img.width / ww
        resized_width = ww / divisor
        resized_height = img.height / ratio /divisor
    }
    else if (img.height > img.width) {
        ratio = img.height / wh
        resized_width = img.width / ratio / divisor
        resized_height = wh / divisor
    }
    else {
        resized_width = ww / divisor
        resized_height = wh / divisor
    }

    return (
        <div>
            <img src={currentImage} style={{height: resized_height+'px', width:resized_width+'px'}}/>
        </div>
    )
}