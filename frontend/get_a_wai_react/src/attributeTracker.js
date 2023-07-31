import React, { useEffect, useState } from 'react';


function AttributeTracker({attributeName, attributeLimit, attributeList}) {
    const [attributeCount, setAttributeCount] = useState(0)

    
    useEffect(()=>{
        setAttributeCount(attributeList.length);
    }, [attributeList])

    return <>
        <div class="card mb-2">
            <div class="card-header d-flex justify-content-between align-items-center">{attributeName} 
            <div>{attributeCount}/{attributeLimit}</div>
            </div>
            <div class="card-body">
                {attributeList.map((attribute, index) => {
                    return <span key={index} class="badge rounded-pill text-bg-secondary ms-1">{attribute}</span>
                })}
            </div> 
        </div>
    </>
}
export default AttributeTracker