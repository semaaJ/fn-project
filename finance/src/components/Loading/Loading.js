import './Loading.css';

const Loading = (props) => {
    const { className, loadType } = props;
    if (loadType === 1) {
        return (
            <div className={`load ${className}`}>
                <hr/><hr/><hr/><hr/>
            </div>
        )
    } else if (loadType === 2) {
        return (
            <div class="load-3">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>
        )
    }
   
}

export default Loading;