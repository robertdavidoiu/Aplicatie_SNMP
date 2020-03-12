from workers import task


@task()
def say_hello(name):
    print('Howdy', name)
