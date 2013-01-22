alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'

function __transcode {
    if [ $# -ne 5 ]; then
        echo "Usage: __transcode <input file> <output file> <bitrate> <codec> <container>"
        return
    fi

    input_file=$1
    output_file=$2
    bitrate=$3
    codec=$4
    container=$5
    vlc -I dummy ${input_file} :sout=#transcode\{acodec=${codec},ab=${bitrate}\}:standard\{mux=${container},dst=${output_file},access=file\} vlc://quit
}

function transcode2mp3 {
    if [ $# -ne 3 ]; then
        echo "Usage: transcode2mp3 <input file> <output file> <bitrate>"
        return
    fi

    input_file=$1
    output_file=$2
    bitrate=$3

    __transcode ${input_file} ${output_file} ${bitrate} mp3 raw
}

function transcode2ogg {
    if [ $# -ne 3 ]; then
        echo "Usage: transcode2ogg <input file> <output file> <bitrate>"
        return
    fi

    input_file=$1
    output_file=$2
    bitrate=$3

    __transcode ${input_file} ${output_file} ${bitrate} vorb ogg
}