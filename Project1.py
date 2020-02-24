import numpy as np
import math
import matplotlib.pyplot as plt
import multiprocessing

call_rate=np.linspace(0.01,0.3,15)
s = np.random.poisson(lam=(100., 500.), size=(100, 2))

# %% parameter
length_area = 10000
length_BS = 1000
size_LA = range(1, 5)
user = 5000
times = 360
single_BS_paging = 0.06
unit_handover = 0.8

# %% input
location = origin = np.random.uniform(0, 10000, size=(user, 2))
destination = np.random.uniform(0, 10000, size=(user, 2))

# %% output
traffic_paging = 0
traffic_handover = 0


# %% processing
# def move(carrier):
#     distance=carrier[0]
#     speed_1D=carrier[1]
#     location_update=carrier[2]
#     destination=carrier[3]
#     unit_speed=carrier[4]
#     length_LA=carrier[5]
#     distance = distance - speed_1D
#     if distance <= 0:
#         location_update = destination
#         destination = np.random.uniform(0, 10000, size=(1, 2))
#         distance= np.linalg.norm(destination - location_update)
#     else:
#         location_update = location+ speed_1D * unit_speed
#
#     if any(np.floor(location_update / length_LA) !=
#            np.floor(location / length_LA)):
#         crossing = 1
#     return location_update,crossing
def simulation(size_LA,call_rate, location=location, destination=destination):
    unit_paging = single_BS_paging * size_LA * size_LA
    length_LA = length_BS * size_LA
    distance = list(map(lambda origin, destination: np.linalg.norm(destination - origin),
                        origin, destination))
    direction = list(map(lambda origin, destination: math.atan2(destination[0] - origin[0], destination[1] - origin[1]),
                         origin, destination))
    unit_speed = list(map(lambda direction: [math.cos(direction), math.sin(direction)],
                          direction))
    unit_speed = np.array(unit_speed)
    traffic_paging = np.zeros(times)
    traffic_handover = np.zeros(times)
    for t in range(times):
        voice_call = np.random.poisson(lam=call_rate, size=user)
        traffic_paging[t] = len(list(filter(lambda x: x != 0, voice_call))) * unit_paging
        speed_1D = np.random.uniform(low=0, high=10, size=user)
        location_update = location.copy()
        crossing = 0
        for i in range(user):
            distance[i] = distance[i] - speed_1D[i]
            if distance[i] <= 0:
                location_update[i] = destination[i]
                destination[i] = np.random.uniform(0, 10000, size=(1, 2))
                distance[i] = np.linalg.norm(destination[i] - location_update[i])
                direction[i] = math.atan2(destination[i][0] - location_update[i][0],
                                          destination[i][1] - location_update[i][1])
                unit_speed[i] = np.array([math.cos(direction[i]), math.sin(direction[i])])
            else:
                location_update[i] = location[i] + speed_1D[i] * unit_speed[i]

            if any(np.floor(location_update[i] / length_LA) !=
                   np.floor(location[i] / length_LA)):
                crossing = crossing + 1
        # cores = multiprocessing.cpu_count()
        # print(cores)
        # pool = multiprocessing.Pool(processes=cores)
        # aa=np.ones(time)*length_LA
        # bb=[distance,speed_1D,location_update,destination,unit_speed]
        # cc=zip(aa,bb)
        # for temp in pool.imap_unordered(move,cc):
        #     crossing=crossing+temp[1]
        #     location_update[i]=temp[0]
        location = location_update.copy()
        traffic_handover[t] = crossing * unit_handover
    #np.savez('pj1_sizeLA=' + str(size_LA), traffic_handover, traffic_paging, user, times)
    return sum(traffic_paging)/times, sum(traffic_handover)/times


def function1():

    data_traffic=np.zeros([len(size_LA),len(call_rate)])

    for i in range(len(size_LA)):
        print("\ni"+str(i))
        for j in range(len(call_rate)):
            print("j"+str(j))
            traffic_paging, traffic_handover = simulation(size_LA[i],call_rate[j])
            data_traffic[i][j]=traffic_paging+traffic_handover
    np.savez('data_traffic', data_traffic, user, times)
            # print("For the size of an LA to be ", i, " km", i, " km, the paging traffic is ",
            #       traffic_paging, "Mbps, the handover traffic is ", traffic_handover,
            #       "Mbps")


def function1_graph():
    # fig, axes = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
    # for i in range(1,5):
    #     a=np.load('pj1_sizeLA='+str(i)+'.npz')
    #     traffic_handover=a['arr_0']
    #     traffic_paging=a['arr_1']
    #     user=a['arr_2']
    #     time=a['arr_3']
    #     axes[i-1].plot(range(time),traffic_handover,'o-', label='handover traffic')
    #     axes[i-1].plot(range(time), traffic_paging, 'o-', label='paging traffic')
    #     axes[i-1].grid()
    #     axes[i-1].set_xlable('time (s)')
    #     axes[i-1].set_ylable('Traffic (Gbps)')
    #     axes[i-1].legend()
    # plt.savefig(fname='pj1.svg')
    # plt.show()
    # for i in size_LA:
    #     a = np.load('pj1_sizeLA=' + str(i) + '.npz')
    #     traffic_handover = a['arr_0']
    #     traffic_paging = a['arr_1']
    #     user = a['arr_2']
    #     time = a['arr_3']
    #     plt.figure()
    #     plt.plot(range(time), traffic_handover, 'o-', label='handover traffic')
    #     plt.plot(range(time), traffic_paging, 'o-', label='paging traffic')
    #     plt.grid()
    #     plt.xlabel('time(s)')
    #     plt.ylabel('Traffic of ' + str(i) + '_' + str(i) + 'LA' + '(Gbps)')
    #     plt.legend()
    #     plt.savefig(fname='pj1_' + str(i) + '_' + str(i) + 'LA.svg')
    #     plt.savefig(fname='pj1_' + str(i) + '_' + str(i) + 'LA.png')
    #     plt.show()
    a = np.load('data_traffic.npz')
    data_traffic = a['arr_0']
    user = a['arr_1']
    time = a['arr_2']
    plt.figure()
    for i in range(len(size_LA)):
        plt.semilogy(call_rate,data_traffic[i],'o-', label="tracking area"+str(i+1)+"*"+str(i+1))
    plt.legend()
    plt.grid()
    plt.xlabel('Expectation of paging frequency (times/s)')
    plt.ylabel('Data traffic (Mbps)')
    plt.title('Control panel traffic (paging+location update)')
    plt.savefig(fname='pj2.svg')
    plt.savefig(fname='pj2.png')
    plt.show()



def main():
    function1()
    function1_graph()


if __name__ == '__main__':
    main()
