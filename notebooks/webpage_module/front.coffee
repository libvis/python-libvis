
import React from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default Vis = ({data, setattr})->
    {addr} = data
    L.div style:display:'contents',
        "Webpage #{addr}"
        L.input type:'text', onChange:(e)=>
                setattr 'text', e.target.value
        L.iframe src:addr
