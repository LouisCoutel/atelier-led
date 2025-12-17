import logging
import socket
import struct

from asyncio import sleep
from asyncio.exceptions import CancelledError
from aiohttp import ClientConnectionResetError

from api.affichage import Affichage


def ddp_header(sequence_number: int, offset: int, packet_size: int):
    return struct.pack(
        "!BBBBLH", 0x40, sequence_number, 0x01, 0x01, offset, packet_size
    )


def send_chunks(chunks, seq, sock, ip, port):
    for i, chunk in enumerate(chunks):
        data = chunk.ravel()
        offset = len(data) * i
        send_ddp_frame(data, seq, offset, sock, ip, port)


async def stream_ddp(
    playlist,
    affichage: Affichage,
    fps: int = 24,
    port: int = 4048,
):
    try:
        seq = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for frame in playlist:
            send_chunks(frame.blocs, seq, sock, affichage.ip, port)

            seq = (seq + 1) % 255

            await sleep(1 / fps)

    except CancelledError:
        logging.info("Websocket was closing.")
        pass

    except ClientConnectionResetError:
        logging.info("Websocket was resetting.")
        pass

    except Exception as e:
        logging.error(e, exc_info=True)
        raise


def send_ddp_frame(
    data,
    sequence_number: int,
    offset: int,
    sock: socket.socket,
    ip: str,
    port: int = 4048,
):
    header = ddp_header(sequence_number, offset, len(data))
    packet = header + data.tobytes()

    sock.sendto(packet, (ip, port))
