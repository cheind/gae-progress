/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
/*
 * This code was generated by https://github.com/google/apis-client-generator/
 * (build: 2016-01-08 17:48:37 UTC)
 * on 2016-01-15 at 07:02:12 UTC 
 * Modify at your own risk.
 */

package com.appspot.progress_1181.progressApi.model;

/**
 * Model definition for ProgressModelsProgressResponseMessage.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the progressApi. For a detailed explanation see:
 * <a href="https://developers.google.com/api-client-library/java/google-http-java-client/json">https://developers.google.com/api-client-library/java/google-http-java-client/json</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class ProgressModelsProgressResponseMessage extends com.google.api.client.json.GenericJson {

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String created;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String description;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key @com.google.api.client.json.JsonString
  private java.lang.Long id;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String lastUpdated;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Double progress;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String title;

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getCreated() {
    return created;
  }

  /**
   * @param created created or {@code null} for none
   */
  public ProgressModelsProgressResponseMessage setCreated(java.lang.String created) {
    this.created = created;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getDescription() {
    return description;
  }

  /**
   * @param description description or {@code null} for none
   */
  public ProgressModelsProgressResponseMessage setDescription(java.lang.String description) {
    this.description = description;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getId() {
    return id;
  }

  /**
   * @param id id or {@code null} for none
   */
  public ProgressModelsProgressResponseMessage setId(java.lang.Long id) {
    this.id = id;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getLastUpdated() {
    return lastUpdated;
  }

  /**
   * @param lastUpdated lastUpdated or {@code null} for none
   */
  public ProgressModelsProgressResponseMessage setLastUpdated(java.lang.String lastUpdated) {
    this.lastUpdated = lastUpdated;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Double getProgress() {
    return progress;
  }

  /**
   * @param progress progress or {@code null} for none
   */
  public ProgressModelsProgressResponseMessage setProgress(java.lang.Double progress) {
    this.progress = progress;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getTitle() {
    return title;
  }

  /**
   * @param title title or {@code null} for none
   */
  public ProgressModelsProgressResponseMessage setTitle(java.lang.String title) {
    this.title = title;
    return this;
  }

  @Override
  public ProgressModelsProgressResponseMessage set(String fieldName, Object value) {
    return (ProgressModelsProgressResponseMessage) super.set(fieldName, value);
  }

  @Override
  public ProgressModelsProgressResponseMessage clone() {
    return (ProgressModelsProgressResponseMessage) super.clone();
  }

}
