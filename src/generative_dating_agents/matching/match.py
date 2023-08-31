# import os
#
# from ..database.chroma import QueryResult, query_user_profile_collection
# from ..utils.io import UserProfile, read_user_profile_from_json
#
#
# def match(user_id: str) -> None:
#     """
#     current best strategy is to do a vector lookup for 20 closest profiles
#     then ask AI to pick the best match. Remove that match from the list. Repeat.
#     this works better than trying to have the model rank, sort, or pick a subset.
#     set temp to 0
#     strip convos
#     :param user_id:
#     :return:
#     """
#     query_user_profile_file_path: str = os.path.join(
#         os.getcwd(), "profiles", user_id, "profile.json"
#     )
#     query_user_profile: UserProfile = read_user_profile_from_json(
#         file_path=query_user_profile_file_path
#     )
#     query_user_profile_summary: str = query_user_profile.profile_summary
#     query_user_preferences_summary: str = query_user_profile.preferences_summary
#     query_result: QueryResult = query_user_profile_collection(
#         collection_name="user_profiles",
#         query_texts=query_user_profile.preferences_summary,
#         n_results=20,
#     )
#     print()
#     print(
#         f"[{user_id}]",
#         (
#             query_user_profile_summary.strip() + " " + query_user_preferences_summary
#         ).strip(),
#     )
#     print()
#     for i in range(len(query_result["ids"][0])):
#         print(
#             f"[{query_result['ids'][0][i]}]",
#             query_result["documents"][0][i].strip()
#             + " "
#             + query_result["metadatas"][0][i]["preferences_summary"].strip(),
#         )
#         print()
#
#
# match(user_id="f0e35556-8760-41ae-b0f9-4c777c48b170")
