import './Loading.css';

const Loading = (props) => {
    const { className } = props;
    return (
        <div className={`load ${className}`}>
            <hr/><hr/><hr/><hr/>
        </div>
    )
}

export default Loading;