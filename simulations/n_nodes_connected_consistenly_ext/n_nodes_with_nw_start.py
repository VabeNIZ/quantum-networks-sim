from multiprocessing import Process, Manager

from time import sleep, time
from common.network import setup_network
from simulations.n_nodes_connected_consistenly_ext.machine import Machine, MachineManager


def main():
    n_nodes = 10
    topology_type = "path"
    network = setup_network(n_nodes, topology_type, keyboard_interrupt=False)
    t1 = time()

    run_nodes_path(n_nodes)

    t2 = time()
    network.stop()
    print(f"Time for {n_nodes} nodes in {topology_type} is {round(t2 - t1, 2)} s")


def run_nodes_path(n_nodes):

    machine_manager_name = 'Manager'
    node_procs = []
    machines = []
    processes_manager = Manager()
    mutex = processes_manager.Lock()

    for i in range(n_nodes):
        # Creating machine
        machine = Machine(f"Node{i + 1}", machine_manager_name, mutex)
        machines.append(machine)

        # Creating and starting process
        proc = Process(target=machine.wait_for_a_command)
        proc.start()
        node_procs.append(proc)

    node_manager = MachineManager(machine_manager_name)
    manager_response_wait_proc = Process(target=node_manager.transmit_key_path_commands, kwargs={'nodes': machines})

    manager_response_wait_proc.start()
    node_procs += [manager_response_wait_proc]

    for p in node_procs:
        p.join()


if __name__ == '__main__':
    main()
