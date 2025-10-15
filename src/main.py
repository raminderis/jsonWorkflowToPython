import asyncio
import argparse, json
from sut_management import SUTManager
from test_management import TESTManager, RESULTSManager

async def get_session_state(test_session_id):
    # Placeholder for getting session state
    test_manager = TESTManager()
    session_info = test_manager.get_session(test_session_id)
    return session_info.get("status", "unknown")

async def fetch_tram_result():
    # Placeholder for fetching TRAM result
    await asyncio.sleep(5)
    return {"result": "sample_result"}

async def publish_tram_results(results):
    # Placeholder for publishing TRAM results
    print(f"Publishing TRAM results to Kafka: {results}")
    await asyncio.sleep(1)
    return True

async def handle_state_change(result):
    print(f"Handling state change: {result}")

    match result:
        case "IN PROGRESS":
            print("Test is in progress...")
            print("Fetching TRAM results...")
            tram_results = await fetch_tram_result()
            print(f"TRAM Results: {tram_results}")
            print("Publishing intermediate results...")
            await publish_tram_results(tram_results)

        case "COMPLETED":
            print("Fetching final TRAM results...")
            tram_results = await fetch_tram_result()
            print(f"Final TRAM Results: {tram_results}")
            print("Publishing final results...")
            await publish_tram_results(tram_results)

        case "ERROR":
            print("Test has encountered an error.")

        case "UNAVAILABLE":
            print("Test session is unavailable.")

        case "PAUSED":
            print("Test session is paused. User to take action — we will wait for 10 seconds.")
            await asyncio.sleep(10)

        case _:
            print(f"No specific handler for session state: {result}")

poll_interval = 10  # seconds

async def main(config):
    sut_manager = SUTManager()

    # TASK 1: set_sut_reservation
    # TASK 2: set_sut_reservation_decision
    workflow_id = config.get("workflow", {}).get("workflowId", "workflow_123")
    user_name = config.get("workflow", {}).get("input", {}).get("security", {}).get("username", "user_abc")
    sut_name = config.get("workflow", {}).get("input", {}).get("test", {}).get("parameters", {}).get("Ts0Tc0", {}).get("MmeSut", "default_sut")
    test_name = config.get("workflow", {}).get("input", {}).get("test", {}).get("name", "default_test")
    test_tas = config.get("workflow", {}).get("input", {}).get("test", {}).get("tas", "default_tas")
    test_servers = config.get("workflow", {}).get("input", {}).get("test", {}).get("testServers", ["default_server"])
    test_libraryId = config.get("workflow", {}).get("input", {}).get("test", {}).get("libraryId", 0)
    parameters = config.get("workflow", {}).get("input", {}).get("test", {}).get("parameters", {})
    print(f"Workflow ID: {workflow_id}, User Name: {user_name}, SUT Name: {sut_name}")
    try:
        sutReservationResponse = sut_manager.reserve_sut(sut_name, workflow_id, user_name)
        print(f"SUT Reservation Response: {sutReservationResponse}")
    except Exception as e:
        print(f"Error reserving SUT: {e}")
        print(f"SUT is busy or not available. Terminating the workflow.")
        # exit(1)

    # Get all reserved SUTs
    reserved_suts = sut_manager.get_all_suts_reserved()
    print(f"All Reserved SUTs: {reserved_suts}")

    

    # TASK 3: create_test_session
    test_manager = TESTManager()
    test_session_response = test_manager.create_testSession(test_name, test_tas, test_servers, test_libraryId)
    if test_session_response is not None:
        test_session_id = test_session_response.get("id")
        print(f"Test session created for Test Name: {test_name} with Session ID: {test_session_id}")
    else:
        print(f"Failed to create test session for Test Name: {test_name}")
        exit(1)
    

    # TASK 4: execute_test
    if test_manager.run_test(test_session_id, parameters):
        print(f"Test started for Test Name: {test_name} with Session ID: {test_session_id}")
    else:
        print(f"Failed to run test for Test Name: {test_name}")
        exit(1)

    # Task 5: handle_execution_state
    known_session_state = "NONE"
    intervalCounter = 0
    while True and intervalCounter < 20:
        try:
            new_session_state = await get_session_state(test_session_id)
            if new_session_state != known_session_state:
                print(f"Session state changed from {known_session_state} to {new_session_state}")
                await handle_state_change(new_session_state)
                known_session_state = new_session_state
            if known_session_state in ["COMPLETED", "ERROR"]:
                print("Session ended.")
                break
            print(f"Waiting for {poll_interval} seconds before next state check...")
            intervalCounter += 1
            await asyncio.sleep(poll_interval)
        except Exception as e:
            print(f"Error while checking session state: {e}")
            await asyncio.sleep(poll_interval)

    # TASK 6: remove_sut_reservation
    reserved_suts = sut_manager.get_all_suts_reserved()
    sutId = reserved_suts.get(sut_name)
    try:
        sutRemovalResponse = sut_manager.remove_sut(sutId)
        print(f"SUT Removal Response: {sutRemovalResponse}")
    except Exception as e:
        print(f"Error removing SUT: {e}")
        exit(1)

    # Get all reserved SUTs
    reserved_suts = sut_manager.get_all_suts_reserved()
    print(f"All Reserved SUTs: {reserved_suts}")


    print("Workflow completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SUT and Test Management Workflow")
    parser.add_argument("--config", "-c", default="config.json", help="Path to the config file")
    args = parser.parse_args()
    config_path = args.config
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    asyncio.run(main(config))