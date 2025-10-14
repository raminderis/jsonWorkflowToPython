from sut_management import SUTManager
from test_management import TESTManager, RESULTSManager

def main():
    sut_manager = SUTManager()

    # Reserve a SUT
    sut_name = "example_sut"
    workflow_id = "workflow_123"
    user_name = "user_abc"
    try:
        sut_id = sut_manager.reserve_sut(sut_name, workflow_id, user_name)
        print(f"Reserved SUT ID: {sut_id}")
    except Exception as e:
        print(f"Error reserving SUT: {e}")
        print(f"SUT is busy or not available. Terminating the workflow.")
        # exit(1)

    # Get all reserved SUTs
    reserved_suts = sut_manager.get_all_suts_reserved()
    print(f"All Reserved SUTs: {reserved_suts}")

    # Create a test session
    test_manager = TESTManager()
    test_id = "test_456"
    if test_manager.create_testSession(test_id):
        print(f"Test session created for Test ID: {test_id}")
    else:
        print(f"Failed to create test session for Test ID: {test_id}")
        exit(1)
    
    # Run the test
    if test_manager.run_test(test_id):
        print(f"Test running for Test ID: {test_id}")
    else:
        print(f"Failed to run test for Test ID: {test_id}")
        exit(1)

    # Get the test session results
    results_manager = RESULTSManager()
    results = results_manager.get_tram_results(test_id)
    print(f"Test results for Test ID {test_id}: {results}")

    print("evaluate results and decide pass/fail...")
    print("in progress publish to Kafka...")
    print("publish results... done")
    print("proceed with cleanup...")
    # Stop the test
    if test_manager.stop_test(test_id):
        print(f"Test stopped for Test ID: {test_id}")
    else:
        print(f"Failed to stop test for Test ID: {test_id}")
        exit(1)

    # Delete the test session
    if test_manager.delete_testSession(test_id):
        print(f"Test session deleted for Test ID: {test_id}")
    else:
        print(f"Failed to delete test session for Test ID: {test_id}")
        exit(1)

    # Remove the reserved SUT
    sut_id = 1
    try:
        sut_manager.remove_sut(sut_id)
        print(f"SUT ID {sut_id} successfully removed.")
    except Exception as e:
        print(f"Failed to remove SUT ID {sut_id} with error: {e}")


if __name__ == "__main__":
    main()