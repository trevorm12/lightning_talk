# the goal is to determine the average wait time for people getting their COVID-19 Vaccines at UT Austin

import simpy
import random

NUM_NURSES = 50
VACCINE_TIME = 5
PAPER_TIME = 15
CHECK_TIME = 10
WAIT_TIME = 15
APPT_INTER = 5
INIT_NUM_PEOPLE = 25
SIM_TIME = 120

class vaccineCenter(object):
    def __init__(self, env, num_nurses, vaccine_time, paper_time, check_time, wait_time):
        self.env = env
        self.nurse = simpy.Resource(env, num_nurses)
        self.vaccination_time = vaccine_time
        self.paperwork_time = paper_time
        self.reaction_check_time = check_time
        self.waiting_time = wait_time

    def wait_in_line(self, person):
        yield self.env.timeout(random.randint(self.waiting_time-2, self.waiting_time+3))

    def fill_paperwork(self, person):
        yield self.env.timeout(random.randint(self.paperwork_time - 2, self.paperwork_time + 3))

    def get_microchip_implanted(self, person):
        yield self.env.timeout(random.randint(self.vaccination_time - 2, self.paperwork_time + 3))

    def wait_for_reaction(self, person):
        yield self.env.timeout(random.randint(self.reaction_check_time - 2, self.reaction_check_time + 3))


def person(env, name, vc):
    print('%s arrives at the vaccine center at %.2f.' % (name, env.now))
    with vc.nurse.request() as request:
        yield request

        print('%s enters the vaccine center at %.2f.' % (name, env.now))
        yield env.process(vc.wait_in_line(name))
        yield env.process(vc.fill_paperwork(name))
        yield env.process(vc.get_microchip_implanted(name))
        yield env.process(vc.wait_for_reaction(name))

        print('%s leaves the vaccine center at %.2f.' % (name, env.now))


def setup(env, num_nurses, vaccine_time, paper_time, check_time, wait_time, appointment_inter):
    """Create a vaccine center, a number of initial people and keep creating people
    approx. every ``appointment_inter`` minutes."""
    # Create the vaccine center
    center = vaccineCenter(env, num_nurses, vaccine_time, paper_time, check_time, wait_time)

    # Create 4 initial cars
    for i in range(INIT_NUM_PEOPLE):
        env.process(person(env, 'Person %d' % i, center))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(appointment_inter - 2, appointment_inter + 2))
        i += 1
        env.process(person(env, 'Person %d' % i, center))


env = simpy.Environment()
env.process(setup(env, NUM_NURSES, VACCINE_TIME, PAPER_TIME, CHECK_TIME, WAIT_TIME, APPT_INTER))

env.run(until=SIM_TIME)
