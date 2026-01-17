# Auto generate by AUTO-GENERATE script
import enum
import socket


class AddressFamily(enum.IntEnum):
    AppleTalk = socket.AF_APPLETALK
    Bluetooth = socket.AF_BLUETOOTH
    HyperV = socket.AF_HYPERV
    INet = socket.AF_INET
    INet6 = socket.AF_INET6
    IPX = socket.AF_IPX
    IRDA = socket.AF_IRDA
    Link = socket.AF_LINK
    SNA = socket.AF_SNA
    UnSpec = socket.AF_UNSPEC


class AddressInfoFlags(enum.IntFlag):
    AddrConfig = socket.AI_ADDRCONFIG
    All = socket.AI_ALL
    CanonName = socket.AI_CANONNAME
    NumericHost = socket.AI_NUMERICHOST
    NumericService = socket.AI_NUMERICSERV
    Passive = socket.AI_PASSIVE
    V4Mapped = socket.AI_V4MAPPED


class BluetoothAddress(enum.StrEnum):
    Any = socket.BDADDR_ANY
    Local = socket.BDADDR_LOCAL


class AddressInfo(enum.IntEnum):
    Again = socket.EAI_AGAIN
    BadFlags = socket.EAI_BADFLAGS
    Fail = socket.EAI_FAIL
    Family = socket.EAI_FAMILY
    Memory = socket.EAI_MEMORY
    NoData = socket.EAI_NODATA
    NoName = socket.EAI_NONAME
    Service = socket.EAI_SERVICE
    SockType = socket.EAI_SOCKTYPE


class HyperVSocket(enum.IntEnum):
    AddressFlagPassthru = socket.HVSOCKET_ADDRESS_FLAG_PASSTHRU
    ConnectedSuspend = socket.HVSOCKET_CONNECTED_SUSPEND
    ConnectTimeout = socket.HVSOCKET_CONNECT_TIMEOUT
    ConnectTimeoutMax = socket.HVSOCKET_CONNECT_TIMEOUT_MAX


class HyperVGUIDs(enum.StrEnum):
    Broadcast = socket.HV_GUID_BROADCAST
    Children = socket.HV_GUID_CHILDREN
    Loopback = socket.HV_GUID_LOOPBACK
    Parent = socket.HV_GUID_PARENT
    Wildcard = socket.HV_GUID_WILDCARD
    Zero = socket.HV_GUID_ZERO


class InternetAddress(enum.IntEnum):
    AllHostsGroup = socket.INADDR_ALLHOSTS_GROUP
    Any = socket.INADDR_ANY
    Broadcast = socket.INADDR_BROADCAST
    Loopback = socket.INADDR_LOOPBACK
    MaxLocalGroup = socket.INADDR_MAX_LOCAL_GROUP
    NoneAddr = socket.INADDR_NONE
    UnspecGroup = socket.INADDR_UNSPEC_GROUP


class IPPort(enum.IntEnum):
    ReServiceed = socket.IPPORT_RESERVED
    UserReServiceed = socket.IPPORT_USERRESERVED


class IPProtocol(enum.IntEnum):
    AH = socket.IPPROTO_AH
    CBT = socket.IPPROTO_CBT
    DSPOPTS = socket.IPPROTO_DSTOPTS
    EGP = socket.IPPROTO_EGP
    ESP = socket.IPPROTO_ESP
    Fragment = socket.IPPROTO_FRAGMENT
    GGP = socket.IPPROTO_GGP
    Hopopts = socket.IPPROTO_HOPOPTS
    ICLFXBM = socket.IPPROTO_ICLFXBM
    ICMP = socket.IPPROTO_ICMP
    ICMPv6 = socket.IPPROTO_ICMPV6
    IDP = socket.IPPROTO_IDP
    IGMP = socket.IPPROTO_IGMP
    IGP = socket.IPPROTO_IGP
    IP = socket.IPPROTO_IP
    IPv4 = socket.IPPROTO_IPV4
    IPv6 = socket.IPPROTO_IPV6
    L2TP = socket.IPPROTO_L2TP
    Max = socket.IPPROTO_MAX
    ND = socket.IPPROTO_ND
    NoneProto = socket.IPPROTO_NONE
    PGM = socket.IPPROTO_PGM
    PIM = socket.IPPROTO_PIM
    PUP = socket.IPPROTO_PUP
    Raw = socket.IPPROTO_RAW
    RDP = socket.IPPROTO_RDP
    Routing = socket.IPPROTO_ROUTING
    SCTP = socket.IPPROTO_SCTP
    ST = socket.IPPROTO_ST
    TCP = socket.IPPROTO_TCP
    UDP = socket.IPPROTO_UDP
    HyperVRaw = socket.HV_PROTOCOL_RAW
    RFCOMM = socket.BTPROTO_RFCOMM


class IPv6Options(enum.IntEnum):
    __level__ = socket.SOL_IP
    CheckSum = socket.IPV6_CHECKSUM
    DontFrag = socket.IPV6_DONTFRAG
    HopLimit = socket.IPV6_HOPLIMIT
    Hopopts = socket.IPV6_HOPOPTS
    JoinGroup = socket.IPV6_JOIN_GROUP
    LeaveGroup = socket.IPV6_LEAVE_GROUP
    MulticastHops = socket.IPV6_MULTICAST_HOPS
    MulticastIf = socket.IPV6_MULTICAST_IF
    MulticastLoop = socket.IPV6_MULTICAST_LOOP
    PacketInfo = socket.IPV6_PKTINFO
    RecvRTHDR = socket.IPV6_RECVRTHDR
    RecvtClass = socket.IPV6_RECVTCLASS
    RTHDR = socket.IPV6_RTHDR
    TClass = socket.IPV6_TCLASS
    UnicastHops = socket.IPV6_UNICAST_HOPS
    V6Only = socket.IPV6_V6ONLY


class IPOptions(enum.IntEnum):
    __level__ = socket.SOL_IP
    AddMembership = socket.IP_ADD_MEMBERSHIP
    AddSourceMembership = socket.IP_ADD_SOURCE_MEMBERSHIP
    BlockSource = socket.IP_BLOCK_SOURCE
    DropMemberShip = socket.IP_DROP_MEMBERSHIP
    DropSourceMemberShip = socket.IP_DROP_SOURCE_MEMBERSHIP
    HDRINCL = socket.IP_HDRINCL
    MulticastIf = socket.IP_MULTICAST_IF
    MulticastLoop = socket.IP_MULTICAST_LOOP
    MulticastTTL = socket.IP_MULTICAST_TTL
    Options = socket.IP_OPTIONS
    Pktinfo = socket.IP_PKTINFO
    RecvDstAddr = socket.IP_RECVDSTADDR
    RecvTos = socket.IP_RECVTOS
    TOS = socket.IP_TOS
    TTL = socket.IP_TTL
    UnblockSource = socket.IP_UNBLOCK_SOURCE


class MessageFlags(enum.IntFlag):
    Boardcast = socket.MSG_BCAST
    Ctrunc = socket.MSG_CTRUNC
    DontRoute = socket.MSG_DONTROUTE
    ErrorQueue = socket.MSG_ERRQUEUE
    Multicast = socket.MSG_MCAST
    OOB = socket.MSG_OOB
    Peek = socket.MSG_PEEK
    Truncate = socket.MSG_TRUNC
    WaitAll = socket.MSG_WAITALL


class NameInfoFlags(enum.IntFlag):
    UDP = socket.NI_DGRAM
    MaxHost = socket.NI_MAXHOST
    MaxService = socket.NI_MAXSERV
    NameReqD = socket.NI_NAMEREQD
    NoFQDN = socket.NI_NOFQDN
    NumericHost = socket.NI_NUMERICHOST
    NumericService = socket.NI_NUMERICSERV


class ReceiveAll(enum.IntEnum):
    Max = socket.RCVALL_MAX
    Off = socket.RCVALL_OFF
    On = socket.RCVALL_ON
    SocketLevelOnly = socket.RCVALL_SOCKETLEVELONLY


class ShutdownHow(enum.IntEnum):
    RD = socket.SHUT_RD
    RDWR = socket.SHUT_RDWR
    WR = socket.SHUT_WR


class SocketIOControl(enum.IntEnum):
    KeepAliveVals = socket.SIO_KEEPALIVE_VALS
    LoopbackFastPath = socket.SIO_LOOPBACK_FAST_PATH
    Rcvall = socket.SIO_RCVALL


class SocketKind(enum.IntEnum):
    UDP = socket.SOCK_DGRAM
    Raw = socket.SOCK_RAW
    Rdm = socket.SOCK_RDM
    SeqPacket = socket.SOCK_SEQPACKET
    TCP = socket.SOCK_STREAM


class SocketLevel(enum.IntEnum):
    IP = socket.SOL_IP
    Socket = socket.SOL_SOCKET
    TCP = socket.SOL_TCP
    UDP = socket.SOL_UDP


class SocketOptions(enum.IntEnum):
    __level__ = socket.SOL_SOCKET
    AcceptConn = socket.SO_ACCEPTCONN
    Broadcast = socket.SO_BROADCAST
    Debug = socket.SO_DEBUG
    DontRoute = socket.SO_DONTROUTE
    Error = socket.SO_ERROR
    ExclusiveAddrUse = socket.SO_EXCLUSIVEADDRUSE
    KeepAlive = socket.SO_KEEPALIVE
    Linger = socket.SO_LINGER
    OOBInline = socket.SO_OOBINLINE
    RcvBuf = socket.SO_RCVBUF
    RcvLowat = socket.SO_RCVLOWAT
    RcvTimeout = socket.SO_RCVTIMEO
    ReuseAddr = socket.SO_REUSEADDR
    SndBuf = socket.SO_SNDBUF
    SndLowat = socket.SO_SNDLOWAT
    SndTimeout = socket.SO_SNDTIMEO
    Type = socket.SO_TYPE
    UseLoopback = socket.SO_USELOOPBACK


class TCPOptions(enum.IntEnum):
    __level__ = socket.SOL_TCP
    FastOpen = socket.TCP_FASTOPEN
    KeepCnt = socket.TCP_KEEPCNT
    KeepIDLE = socket.TCP_KEEPIDLE
    KeepIntvl = socket.TCP_KEEPINTVL
    MaxSegment = socket.TCP_MAXSEG
    NoDelay = socket.TCP_NODELAY
