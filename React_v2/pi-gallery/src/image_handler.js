import React, { useEffect, useState } from "react";
import img0 from './imgs/1.PNG'
import img1 from './imgs/2.PNG'
import img2 from './imgs/3.png'
import img3 from './imgs/4.png'
import img4 from './imgs/5.png'
import img5 from './imgs/6.png'
import img6 from './imgs/7.png'
import gif0 from './imgs/2_1.gif'
import gif1 from './imgs/2_2.gif'

const divisor = 2.5
const image_info = [
    {
        img: img0,
        width: 0,
        height: 0
    },
    {
        img: img1,
        width: 0,
        height: 0
    },
    {
        img: img2,
        width: 0,
        height: 0
    },
    {
        img: img3,
        width: 0,
        height: 0
    },
    {
        img: img4,
        width: 0,
        height: 0
    },
    {
        img: img5,
        width: 0,
        height: 0
    },
    {
        img: img6,
        width: 0,
        height: 0
    },
    {
        img: gif0,
        width: 0,
        height: 0
    },
    {
        img: gif1,
        width: 0,
        height: 0
    }
]

function resizeImages() {
    let ratio;
    let resized_height;
    let resized_width;

    const wh = window.innerHeight
    const ww = window.innerWidth

    for (let i = 0; i < image_info.length; i++) {
        let img = new Image();
        img.src = image_info[i].img

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

        image_info[i].width = resized_width
        image_info[i].height = resized_height
    }
    console.log(image_info)
}

export default function ImageSwapper() {
    if (image_info[0].width === 0) {
        resizeImages()
    }

    const [currentIndex, setCurrentIndex] = useState(0);
    const [currentImage, setCurrentImage] = useState(null);
    const [random, setRandom] = useState(true);
    const [key, setKey] = useState("");
    const [change, setChange] = useState(0);

    useEffect(() => {
        window.addEventListener('keypress', e => {
            if (e.key === "s") {
                setRandom(prev => !prev);
                setKey(e.key)
            }
            else {
                setRandom(false)
                setKey(e.key)   
            }
            setChange(prev => prev + 1)
        });
    }, [])

    useEffect(() => {
        let intervalId = null;

        if(random === true) {
            console.log(random, key)
            intervalId = setInterval(() => {
                let i = Math.floor(Math.random() * image_info.length)
                setCurrentIndex(i)
                setCurrentImage(image_info[i]);
            }, 5000)
        }
        else {
            console.log(random, key)
            let newIndex = 0
            if (key === "a") {
                intervalId = setInterval(() => {
                    if(currentIndex === 0) {
                        newIndex = image_info.length - 1
                        setCurrentIndex(newIndex);
                        setCurrentImage(image_info[newIndex]);
                    } 
                    else {
                        newIndex = currentIndex - 1
                        setCurrentIndex(newIndex);
                        setCurrentImage(image_info[newIndex]);
                    }
                }, 10)
            }
            else if (key === "d") {
                intervalId = setInterval(() => {
                    if(currentIndex === image_info.length - 1) {
                        newIndex = 0
                        setCurrentIndex(newIndex);
                        setCurrentImage(image_info[newIndex]);
                    } 
                    else {
                        newIndex = currentIndex + 1
                        setCurrentIndex(newIndex);
                        setCurrentImage(image_info[newIndex]);
                    }
                }, 10)
            }
        }
        
        return () => clearInterval(intervalId);
    }, [random, key, change])
    
    return (
        <div>
               {currentImage && <img src={currentImage.img} style={{height: currentImage.height+'px', width:currentImage.width+'px'}}/>}
        </div>
     )
 }